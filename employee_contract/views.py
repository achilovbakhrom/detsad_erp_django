from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import ValidationError
from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.models import BaseUserCheck, Branch, EmployeeContract
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from employee_contract.filters import EmployeeContractFilter
from employee_contract.serializers import EmployeeContractSerializer, EmployeeContractInputSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

@extend_schema(tags=['Employee Contract'])
class EmployeeContractListView(NonDeletedFilterMixin, TenantFilterMixin, generics.ListAPIView):
    queryset = EmployeeContract.objects.all()
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    serializer_class = EmployeeContractSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__middle_name', 'employee__description']
    filterset_class = EmployeeContractFilter

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


@extend_schema(tags=['Employee Contract'])
class EmployeeContractRetrieveDestroyView(NonDeletedFilterMixin, TenantFilterMixin, generics.RetrieveDestroyAPIView):
    queryset = EmployeeContract.objects.all()
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    serializer_class = EmployeeContractSerializer
    lookup_field = "id"


@extend_schema(tags=['Employee Contract'])
class HireEmployeeView(generics.CreateAPIView, NonDeletedFilterMixin):
    queryset = EmployeeContract.objects.all()
    permission_classes=[IsAuthenticated, HasTenantIdPermission]
    serializer_class=EmployeeContractInputSerializer

@extend_schema(tags=['Employee Contract'])
class ActivateEmployeeContractView(generics.UpdateAPIView, NonDeletedFilterMixin, TenantFilterMixin):
    http_method_names = ['put']
    queryset = EmployeeContract.objects.all()
    serializer_class = EmployeeContractSerializer

    def update(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if not id:
            raise ValidationError({"detail": "ID not provided"})
        
        employee = EmployeeContract.objects.get(id=id)

        employee.status = 'active'
        employee.save()

        seralizer = self.get_serializer(employee)
        

        return Response(seralizer.data)

@extend_schema(tags=['Employee Contract'])
class DeactivateEmployeeContractView(generics.UpdateAPIView, NonDeletedFilterMixin, TenantFilterMixin):
    queryset = EmployeeContract.objects.all()
    serializer_class = EmployeeContractSerializer
    lookup_field = 'id'

@extend_schema(tags=['Employee Contract'])
class FireEmployeeView(generics.DestroyAPIView):
    queryset = EmployeeContract.objects.all()
    serializer_class = EmployeeContractSerializer

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('id')
        if not id:
            raise ValidationError({"detail": "ID not provided"})
        
        employee = EmployeeContract.objects.get(id=id)

        employee.status = 'finished'
        employee.save()

        seralizer = self.get_serializer(employee)
        
        return Response(seralizer.data)
    
    