from rest_framework import viewsets, permissions

from core.utils import error_response, success_response
from .serializers import CompanySerializer
from core.models import Company, CompanyUserRelation
from core.pagination import CustomPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from django.db.models import Q

@extend_schema(tags=['Company'])
class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    queryset = Company.objects.none()
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search by name or inn"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Retrieve companies associated with the currently authenticated user.
        """
        user_id = self.request.user.id
        user_companies = CompanyUserRelation.objects.filter(user_id=user_id).values_list('company_id', flat=True)
        queryset = Company.objects.filter(id__in=user_companies)

        # Apply custom search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(inn__icontains=search)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        body = request.data

        if Company.objects.filter(name=body.get('name')).exists():
            return error_response('A company with this name is already exist', status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=body)

        if not serializer.is_valid():
            return error_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if body.get('is_default'):
            user_companies = CompanyUserRelation.objects.filter(user=user)
            company_ids = map(lambda item: item.company_id, user_companies)
            companies = Company.objects.filter(id__in=company_ids)
            companies.update(is_default=False)

        self.perform_create(serializer)
        created_instance = serializer.instance
        
        CompanyUserRelation.objects.create(user=user, company=created_instance)
        
        return success_response(serializer.data)

    
    def update(self, request, *args, **kwargs):
        user = request.user
        body = request.data

        instance = self.get_object()

        serializer = self.get_serializer(instance, data=body, partial=True)

        if not serializer.is_valid():
            return error_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if body.get('is_default'):
            user_companies = CompanyUserRelation.objects.filter(user=user)
            company_ids = map(lambda item: item.company_id, user_companies)
            companies = Company.objects.filter(id__in=company_ids)
            companies.update(is_default=False)

        self.perform_update(serializer)

        return success_response(serializer.data)

        
            
