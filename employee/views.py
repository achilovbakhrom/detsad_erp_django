from rest_framework import viewsets, permissions, generics, filters
from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.models import BaseUserCheck
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from employee.filters import EmployeeFilterSet
from .serializers import EmployeeInputSerializer, EmployeeSerializer
from core.models import Employee
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from core.utils import success_response, error_response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

@extend_schema(tags=['Employee'])
class EmployeeListView(NonDeletedFilterMixin, TenantFilterMixin, generics.ListAPIView):
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    search_fields = ['first_name', 'last_name', 'middle_name', 'date_of_birth', 'description']
    filter_backends=[DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EmployeeFilterSet
    queryset = Employee.objects.all()

@extend_schema(tags=["Employee"])
class EmployeeRetrieveDestroyView(NonDeletedFilterMixin, TenantFilterMixin, generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = 'id'

@extend_schema(tags=['Employee'])
class EmployeeEditView(NonDeletedFilterMixin, TenantFilterMixin, generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    queryset = Employee.objects.all()
    serializer_class = EmployeeInputSerializer
    lookup_field = "id"

@extend_schema(tags=["Employee"])
class EmployeeCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    queryset = Employee.objects.all()
    serializer_class = EmployeeInputSerializer