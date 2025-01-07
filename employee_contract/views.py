from rest_framework import generics
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import ValidationError, NotFound
from core.models import BaseUserCheck, Branch, EmployeeContract
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.pagination import CustomPagination
from employee_contract.serializers import EmployeeContractSerializer, CreateEmployeeContractSerializer

@extend_schema(
    tags=['Employee Contract'],
    parameters=[
        OpenApiParameter(
            name="company_id",
            required=True,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="filter by company_id"
        ),
        OpenApiParameter(
            name="branch_id",
            required=False,
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="filter by branch_id"
        ),
    ]
)
class EmployeeContractsListView(generics.ListAPIView, BaseUserCheck):
    queryset=EmployeeContract.objects.none()
    permission_classes=[IsAuthenticated]
    serializer_class = EmployeeContractSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        request = self.request
        user_id = request.user.id
        company_id = request.query_params.get('company_id', None)
        (belongs, err_msg) = self.company_belongs_to_user(user_id=user_id, company_id=company_id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })
        
        branch_id = request.query_params.get('branch_id', None)

        if branch_id:
            branches = [branch_id]
        else:
            branches = Branch.objects.filter(company_id=company_id).values_list("id", flat=True)
        
        queryset = EmployeeContract.objects.filter(Q(branch_id__in=branches) & Q(is_deleted=False))

        return queryset

@extend_schema(tags=['Employee Contract'])
class HireEmployeeView(generics.CreateAPIView):
    queryset = EmployeeContract.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=CreateEmployeeContractSerializer

@extend_schema(tags=['Employee Contract'])
class ActivateEmployeeContractView(generics.UpdateAPIView):
    queryset = EmployeeContract.objects.all()
    http_method_names = ['put']
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
class RetrieveEmployeeView(generics.RetrieveAPIView):
    queryset = EmployeeContract.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class = EmployeeContractSerializer
    lookup_field = "id"
    

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
    

@extend_schema(tags=['Employee Contract'])
class DeleteEmployeeView(generics.DestroyAPIView):
    queryset = EmployeeContract.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class = EmployeeContractSerializer
    lookup_field = 'id'
    