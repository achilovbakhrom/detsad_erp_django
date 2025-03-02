import django_filters
from core.models import SickLeave

class SickLeaveFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    date_to = django_filters.CharFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = SickLeave
        fields = ['child_id', 'has_reason']