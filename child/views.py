from rest_framework import permissions, generics, filters
from child.filters import ChildFilterSet
from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from .serializers import ChildInputSerializer, ChildSerializer
from core.models import Child
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

@extend_schema(tags=['Child'])
class ChildListView(NonDeletedFilterMixin, TenantFilterMixin, generics.ListAPIView):
    serializer_class = ChildSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    search_fields = ['first_name', 'last_name', 'middle_name', 'description']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ChildFilterSet
    queryset= Child.objects.all()

@extend_schema(tags=["Child"])
class ChildRetrieveDestroyView(NonDeletedFilterMixin, TenantFilterMixin, generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    serializer_class = ChildSerializer
    queryset= Child.objects.all()
    lookup_field = 'id'

@extend_schema(tags=['Child'])
class ChildEditView(NonDeletedFilterMixin, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    queryset= Child.objects.all()
    serializer_class = ChildInputSerializer
    lookup_field = "id"

@extend_schema(tags=['Child'])
class ChildCreateView(NonDeletedFilterMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    queryset= Child.objects.all()
    serializer_class = ChildInputSerializer
    lookup_field = "id"