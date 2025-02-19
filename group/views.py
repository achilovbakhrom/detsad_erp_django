from rest_framework import permissions, generics, filters

from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from .serializers import GroupInputSerializer, GroupSerializer
from core.models import Group
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend

@extend_schema(tags=['Group'])
class GroupListView(NonDeletedFilterMixin, TenantFilterMixin, generics.ListAPIView):
    serializer_class = GroupSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    search_fields = ['name', 'description']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    queryset = Group.objects.all()

@extend_schema(tags=['Group'])
class GroupRetrieveDestroyView(NonDeletedFilterMixin, TenantFilterMixin, generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    lookup_field = 'id'

@extend_schema(tags=['Group'])
class GroupEditView(NonDeletedFilterMixin, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    queryset = Group.objects.all()
    serializer_class = GroupInputSerializer
    lookup_field = 'id'

@extend_schema(tags=['Group'])
class GroupCreateView(NonDeletedFilterMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    queryset = Group.objects.all()
    serializer_class = GroupInputSerializer
    lookup_field = 'id'