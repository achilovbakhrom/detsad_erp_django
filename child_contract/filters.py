import django_filters
from core.models import ChildContract

class ChildContractFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = ChildContract
        fields = ['branch_id', 'group_registration_id', 'date_from', 'date_to']
