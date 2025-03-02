from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from core.mixins import TenantFilterMixin
from core.models import Transaction
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from transaction.filters import TransactionFilter
from transaction.serializer import TransactionInputSerializer, TransactionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

@extend_schema(tags=['Transaction'])
class TransactionListView(TenantFilterMixin, ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = CustomPagination
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    filterset_class = TransactionFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['payment_type__name', 'account__name']


@extend_schema(tags=['Transaction'])
class TransactionRetrieveDestroyView(TenantFilterMixin, RetrieveDestroyAPIView):
    queryset = Transaction.objects.all()
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    serializer_class = TransactionSerializer
    lookup_field = "id"

@extend_schema(tags=['Transaction'])
class CreateTransactionView(CreateAPIView):
    queryset = Transaction.objects.all()
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    serializer_class = TransactionInputSerializer