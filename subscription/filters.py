import django_filters
from core.models import Subscription

class SubscriptionFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    amount_from = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    amount_to = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')

    class Meta:
        model = Subscription
        fields = ['child_id', 'payment_type_id', 'date_from', 'date_to', 'amount_from', 'amount_to']