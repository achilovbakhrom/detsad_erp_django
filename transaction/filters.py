import django_filters
from core.models import Transaction

class TransactionFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    payment_type_id = django_filters.NumberFilter(field_name="payment_type_id")
    amount_from = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    amount_to = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')
    
    class Meta:
        model = Transaction
        fields = []