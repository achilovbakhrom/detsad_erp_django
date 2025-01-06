# Create your views here.
from rest_framework import viewsets, permissions

from core.pagination import CustomPagination
from core.utils import error_response, success_response
from .serializers import BranchSerializer
from core.models import Branch, BaseUserCheck
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import NotFound, ValidationError
from django.db.models import Q
from rest_framework import status


@extend_schema(tags=['Branch'])
class BranchView(viewsets.ModelViewSet, BaseUserCheck):
    serializer_class = BranchSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset=Branch.objects.none()

    @extend_schema(
            parameters=[
                OpenApiParameter(
                    name="search",
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="Search by name or inn"
                ),
                OpenApiParameter(
                    name="company_id",
                    required=True,
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY,
                    description="filter by company_id"
                ),
            ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    
    def get_queryset(self):
        request = self.request
        user_id = request.user.id
        if request.method == "GET" and self.action == "list":
            
            company_id = request.query_params.get('company_id', None)
            print(f'company id {company_id}')
            (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
            if not belongs:
                raise ValidationError({ "detail": err_msg })
            
            search = request.query_params.get('search', None)
            
            queryset = Branch.objects.filter(Q(company_id=company_id) & Q(is_deleted=False))
            
            if search:
                queryset = queryset.filter(Q(name__icontains=search))

            return queryset
        elif request.method == "GET" and self.action == "retrieve":
            branch_id = self.kwargs.get('pk', None)
            try:
                branch = Branch.objects.get(id=branch_id)
                company_id = branch.company.id
                (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
                if not belongs:
                    raise ValidationError({ "detail": err_msg })
            except Branch.DoesNotExist:
                raise NotFound({ "detail": "branch_id is not found" })
        elif request.method == "DELETE":
            try:

                branch_id = self.kwargs.get('pk', None)
                branch = Branch.objects.get(id=branch_id)
                company_id = branch.company.id
                (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
                if not belongs:
                    raise ValidationError({ "detail": err_msg })
            except Branch.DoesNotExist:
                raise NotFound({ "detail": "branch_id is not found" })

        return Branch.objects.all()
    
    
    def create(self, request, *args, **kwargs):
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
    
    def update(self, request, *args, **kwargs):
        body = request.data        
        instance = Branch.objects.get(pk=kwargs.get('pk', None))
        serializer = self.get_serializer(instance, data=body, partial=True)
        if not serializer.is_valid():
            return error_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        return success_response(serializer.data)
