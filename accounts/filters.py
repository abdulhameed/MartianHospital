import django_filters

from accounts.models import DocProfile


class DocProfileFilter(django_filters.FilterSet):
    user__first_name = django_filters.CharFilter(lookup_expr='icontains')
    user__last_name = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = DocProfile
        fields = ['state']