from requests import Response
from rest_framework import permissions, generics, filters
from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission, get_tenant_id
from .serializers import BranchInputSerializer, BranchSerializer
from core.models import Branch
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema(tags=['Branch'])
class BranchListView(NonDeletedFilterMixin, TenantFilterMixin, generics.ListAPIView):
    serializer_class = BranchSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    search_fields = ['name', 'address', 'description']
    filter_backends=[DjangoFilterBackend, filters.SearchFilter]
    queryset= Branch.objects.all()

@extend_schema(tags=["Branch"])
class BranchRetrieveDestroyView(NonDeletedFilterMixin, TenantFilterMixin, generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    serializer_class = BranchSerializer
    queryset= Branch.objects.all()
    lookup_field = 'id'

@extend_schema(tags=['Branch'])
class BranchEditView(NonDeletedFilterMixin, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    queryset= Branch.objects.all()
    serializer_class = BranchInputSerializer
    lookup_field = "id"

@extend_schema(tags=["Branch"])
class BranchCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    queryset= Branch.objects.all()
    serializer_class = BranchInputSerializer