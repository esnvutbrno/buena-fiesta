from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from elasticsearch import Elasticsearch, Transport, Urllib3HttpConnection

from apps.utils.breadcrumbs import with_breadcrumb


class LocalCATrustedTransportion(Transport):
    # TODO: really here?
    class CATrustedConnection(Urllib3HttpConnection):
        def __init__(self, *args, **kwargs) -> None:
            kwargs["ca_certs"] = "/usr/share/certs/rootCA.pem"
            super().__init__(*args, **kwargs)

    DEFAULT_CONNECTION_CLASS = CATrustedConnection


es = Elasticsearch(
    hosts=["https://elastic:elastic@elastic:9200"],
    transport_class=LocalCATrustedTransportion,
)


@with_breadcrumb(_("Docs"), url_name="wiki:index")
class SearchWikiView(TemplateView):
    template_name = "wiki/search.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = self.request.GET.get("q")
        results = es.search(
            index="wiki",
            query={
                "match_phrase": {
                    "content_plain": q,
                },
                # "multi_match": {
                #     "query": q,
                #     "fields": ["content_plain"],
                #     "fuzziness": "AUTO"
                # }
            },
            highlight={
                "tags_schema": "styled",
                "fields": {
                    "content_plain": {
                        "type": "unified",
                        "matched_fields": ["content_plain"],
                        "number_of_fragments": 1,
                        "fragment_size": 200,
                        # "pre_tags": ["<b>"],
                        # "post_tags": ["</b>"]
                    }
                },
            },
        )

        ctx["results"] = [
            dict(source=hit["_source"], highlight=hit["highlight"], score=hit["_score"])
            for hit in results["hits"]["hits"]
        ]
        ctx["q"] = q

        self.request.titles.append(_("Search results: {}").format(q))

        return ctx


@with_breadcrumb(_("Docs"), url_name="wiki:index")
class WikiView(TemplateView):
    template_name = "wiki/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        sidebar = es.get(index="wiki", id="_Sidebar.md")

        ctx["sidebar"] = sidebar["_source"]

        if path := self.kwargs.get("path"):
            found_hits = es.search(
                index="wiki",
                query=dict(
                    prefix={
                        "file.keyword": path,
                    }
                ),
            )["hits"]["hits"]

            if not found_hits:
                raise Http404(_("Wii page not found."))
            page = found_hits[0]["_source"]
            ctx["page"] = page

            self.request.titles.append(page.get("title"))
        else:
            ctx["page"] = es.get(index="wiki", id="Home.md")["_source"]

        return ctx
