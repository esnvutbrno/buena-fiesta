import django_tables2 as tables
from django.db.models.fields.files import FieldFile
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, ChoiceFilter
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, Column, LazyPaginator

from apps.sections.middleware.user_membership import HttpRequest
from apps.sections.models import SectionMembership
from apps.utils.breadcrumbs import with_breadcrumb


class ImageColumn(tables.Column):
    def render(self, value: FieldFile):
        return format_html(
            '<img src="{}" class="h-12" />',
            value.url
        )


class SectionMembershipFilter(FilterSet):
    state = ChoiceFilter(choices=SectionMembership.State.choices)
    role = ChoiceFilter(choices=SectionMembership.Role.choices)

    class Meta:
        model = SectionMembership
        fields = ['state', 'role']


class MembershipTable(tables.Table):
    user__get_full_name = Column(
        order_by=("user__last_name", "user__first_name", "user__username")
    )

    user__profile__picture = ImageColumn()

    class Meta:
        model = SectionMembership

        fields = (
            "role",
            "state",
            "created"
        )
        sequence = (
            'user__get_full_name',
            'user__profile__picture',
            '...'
        )


@with_breadcrumb(_('Section Members'))
class SectionMembersView(SingleTableMixin, FilterView):
    request: HttpRequest
    template_name = 'accounts/section_members.html'
    table_class = MembershipTable
    filterset_class = SectionMembershipFilter
    paginate_by = 5
    paginator_class = LazyPaginator

    def get_queryset(self):
        return SectionMembership.objects.filter(
            section=self.request.membership.section,
        ).select_related('user__profile')
