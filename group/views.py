from rest_framework import viewsets, permissions

from core.pagination import CustomPagination
from .serializers import GroupSerializer
from core.models import Company, BaseUserCheck, Group
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import ValidationError, NotFound
from django.db.models import Q
from core.utils import success_response, error_response
from rest_framework import status

@extend_schema(tags=['Group'])
class GroupView(viewsets.ModelViewSet, BaseUserCheck):
    serializer_class = GroupSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset=Company.objects.none()

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
            (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
            if not belongs:
                raise ValidationError({ "detail": err_msg })
            
            search = request.query_params.get('search', None)
            
            queryset = Group.objects.filter(Q(company_id=company_id) & Q(is_deleted=False))

            if search:
                queryset = queryset.filter(Q(name__icontains=search))
            return queryset
        
        elif request.method == "GET" and self.action == "retrieve":
            group_id = self.kwargs.get('pk', None)
            try:
                group = Group.objects.get(id=group_id)
                company_id = group.company.id
                (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
                if not belongs:
                    raise ValidationError({ "detail": err_msg })
            except Group.DoesNotExist:
                raise NotFound({ "detail": "group_id is not found" })
        elif request.method == "DELETE":
            try:
                group_id = self.kwargs.get('pk', None)
                group = Group.objects.get(id=group_id)
                company_id = group.company.id
                (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
                if not belongs:
                    raise ValidationError({ "detail": err_msg })
            except Group.DoesNotExist:
                raise NotFound({ "detail": "group_id is not found" })

        return Group.objects.all()
    
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
        instance = Group.objects.get(pk=kwargs.get('pk', None))
        serializer = self.get_serializer(instance, data=body, partial=True)
        if not serializer.is_valid():
            return error_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        return success_response(serializer.data)