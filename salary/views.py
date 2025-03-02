from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.models import Salary
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from salary.filters import SalaryFilter
from salary.serializers import SalaryInputSerializer, SalaryListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

@extend_schema(tags=['Salary'])
class SalaryListView(ListAPIView, TenantFilterMixin, NonDeletedFilterMixin):
    queryset = Salary.objects.all()
    serializer_class = SalaryListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SalaryFilter
    search_fields = ['employee__employee__first_name', 'employee__employee__last_name', 'employee__employee__middle_name']

@extend_schema(tags=['Salary'])
class SalaryRetrieveDestroyView(RetrieveDestroyAPIView, TenantFilterMixin, NonDeletedFilterMixin):
    queryset = Salary.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = SalaryListSerializer
    lookup_field = 'id'

@extend_schema(tags=['Salary'])
class CreateSalaryView(CreateAPIView, NonDeletedFilterMixin):
    queryset = Salary.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = SalaryInputSerializer
    
