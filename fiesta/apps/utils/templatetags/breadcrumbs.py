from __future__ import annotations

from typing import NamedTuple

from django import template
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.plugins.middleware.plugin import HttpRequest

register = template.Library()


class BreadcrumbTitle(NamedTuple):
    title: str
    url: str


@register.simple_tag(takes_context=True)
def breadcrumb_items(context: dict):
    req: HttpRequest = context.get("request")

    if hasattr(req, "breadcrumbs"):
        return req.breadcrumbs

    view: View | None = context.get("view")

    try:
        view_title = view.title
    except AttributeError:
        view_title = None

    req.breadcrumbs = list(
        filter(
            None,
            [
                # TODO: slash is not always the home page?
                BreadcrumbTitle(
                    req.membership.section if req.membership else _("Home"), "/"
                ),
                BreadcrumbTitle(apps.title, f"/{apps.url_prefix}")
                if (plugin := req.plugin) and (apps := plugin.app_config)
                else None,
                BreadcrumbTitle(view_title, req.build_absolute_uri())
                if view_title
                else None,
            ],
        )
    )
    return req.breadcrumbs


@register.simple_tag(takes_context=True)
def breadcrumb_push_item(context: dict, item: str):
    view: View = context["view"]

    view.title = item

    return ""
