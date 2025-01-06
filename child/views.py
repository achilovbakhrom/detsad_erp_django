from rest_framework import viewsets, permissions

from core.pagination import CustomPagination
from .serializers import ChildSerializer
from core.models import Child, BaseUserCheck
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from core.utils import success_response, error_response
from django.db.models import Q


@extend_schema(tags=['Children'])
class ChildView(viewsets.ModelViewSet, BaseUserCheck):
    serializer_class = ChildSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset=Child.objects.none()

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
            
            queryset = Child.objects.filter(Q(company_id=company_id) & Q(is_deleted=False))

            if search:
                queryset = queryset.filter(Q(name__icontains=search))

            return queryset
        elif request.method == "GET" and self.action == "retrieve":
            child_id = self.kwargs.get('pk', None)
            try:
                child = Child.objects.get(id=child_id)
                company_id = child.company.id
                (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
                if not belongs:
                    raise ValidationError({ "detail": err_msg })
            except Child.DoesNotExist:
                raise NotFound({ "detail": "child_id is not found" })
        elif request.method == "DELETE":
            try:

                child_id = self.kwargs.get('pk', None)
                child = Child.objects.get(id=child_id)
                company_id = child.company.id
                (belongs, err_msg) = self.company_belongs_to_user(user_id, company_id)
                if not belongs:
                    raise ValidationError({ "detail": err_msg })
            except Child.DoesNotExist:
                raise NotFound({ "detail": "child_id is not found" })

        return Child.objects.all()
    
    
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

        try:
            self.perform_create(serializer)
        except Child.DoesNotExist:
            raise NotFound({ "detail": "child_id is not found" })

        return success_response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            body = request.data        
            instance = Child.objects.get(pk=kwargs.get('pk', None))
            if instance.is_deleted:
                raise Child.DoesNotExist()
            
            serializer = self.get_serializer(instance, data=body, partial=True)
            if not serializer.is_valid():
                return error_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            self.perform_update(serializer)
        except Child.DoesNotExist:
            raise NotFound({ "detail": "child_id is not found" })

        return success_response(serializer.data)
