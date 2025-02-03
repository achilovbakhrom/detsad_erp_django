from jsonschema import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.models import BaseUserCheck, Branch, Salary
from core.pagination import CustomPagination
from salary.serializers import CreateSalarySerializer, SalaryListSerializer
from django.db.models import Q
from rest_framework import status
from core.utils import success_response, error_response

@extend_schema(
    tags=['Salary'],
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
class SalaryView(ListAPIView, BaseUserCheck):
    permission_classes=[IsAuthenticated]
    queryset = Salary.objects.all()
    serializer_class = SalaryListSerializer
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
        
        queryset = Salary.objects.filter(Q(branch_id__in=branches) & Q(is_deleted=False))

        return queryset


@extend_schema(tags=['Salary'])
class CreateSalaryView(CreateAPIView, BaseUserCheck):
    queryset = Salary.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSalarySerializer

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        body = request.data
        company_id = body.get('company', None)
        (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })

        serializer = self.get_serializer(data = body)

        if not serializer.is_valid():
            return error_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        self.perform_create(serializer)

        return success_response(serializer.data)
    
@extend_schema(tags=['Salary'])
class RetrieveSalaryView(RetrieveAPIView):
    queryset = Salary.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SalaryListSerializer
    lookup_field = 'id'

@extend_schema(tags=['Salary'])
class SalaryDeleteView(DestroyAPIView, BaseUserCheck):
    queryset = Salary.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        id = kwargs.get('id')
        salary = Salary.objects.get(id=id)
        company_id = salary.company.id
        (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })
        return super().destroy(request, *args, **kwargs)