from rest_framework import generics
from drf_spectacular.utils import extend_schema

from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.models import Subscription
from core.pagination import CustomPagination
from subscription.filters import SubscriptionFilter
from subscription.serializers import SubscriptionInputSerializer, SubscriptionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from core.permissions import HasTenantIdPermission

@extend_schema(tags=["Subscription"])
class SubscriptionListView(NonDeletedFilterMixin, TenantFilterMixin, generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    pagination_class = CustomPagination
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    filterset_class = SubscriptionFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['child__child__first_name', 'child__child__last_name', 'child__child__middle_name', 'payment_type__name', 'account__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        # salary_from = self.request.query_params.get('salary_from')
        # salary_to = self.request.query_params.get('salary_to')
        if date_from and date_to:
            queryset = queryset.filter(date__range=[date_from, date_to])
        elif date_from:
            queryset = queryset.filter(date__gte=date_from)
        elif date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        # if salary_from and salary_to:
        #     queryset = queryset.filter(salary__range=[salary_from, salary_to])
        # elif salary_from:
        #     queryset = queryset.filter(salary__gte=salary_from)
        # elif salary_to:
        #     queryset = queryset.filter(salary__lte=salary_to)
        return queryset
    
@extend_schema(tags=["Subscription"])
class SubscriptionRetrieveDestroyView(NonDeletedFilterMixin, TenantFilterMixin, generics.RetrieveDestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    serializer_class = SubscriptionSerializer
    lookup_field = "id"

@extend_schema(tags=["Subscription"])
class CreateSubscriptionView(generics.CreateAPIView, NonDeletedFilterMixin):
    queryset = Subscription.objects.all()
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    serializer_class = SubscriptionInputSerializer