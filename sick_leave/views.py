from jsonschema import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.models import BaseUserCheck, Branch, SickLeave
from core.pagination import CustomPagination
from sick_leave.serializers import CreateSickLeaveSerializer, SickLeaveListSerializer
from django.db.models import Q
from rest_framework import status
from core.utils import success_response, error_response

@extend_schema(
    tags=['Sick Leave'],
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
class SickLeaveView(ListAPIView, BaseUserCheck):
    permission_classes=[IsAuthenticated]
    queryset = SickLeave.objects.all()
    serializer_class = SickLeaveListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        request = self.request
        user_id = request.user.id
        company_id = request.query_params.get('company_id', None)
        (belongs, err_msg) = self.company_belongs_to_user(user_id=user_id, company_id=company_id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })
        
        queryset = SickLeave.objects.filter(company_id=company_id)

        return queryset


@extend_schema(tags=['Sick Leave'])
class CreateSickLeaveView(CreateAPIView, BaseUserCheck):
    queryset = SickLeave.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateSickLeaveSerializer

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
    
@extend_schema(tags=['Sick Leave'])
class RetrieveSickLeaveView(RetrieveAPIView):
    queryset = SickLeave.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = SickLeaveListSerializer
    lookup_field = 'id'

@extend_schema(tags=['Sick Leave'])
class SickLeaveDeleteView(DestroyAPIView, BaseUserCheck):
    queryset = SickLeave.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        id = kwargs.get('id')
        sick_leave = SickLeave.objects.get(id=id)
        company_id = sick_leave.company.id
        (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
        if not belongs:
            raise ValidationError({ "detail": err_msg })
        return super().destroy(request, *args, **kwargs)