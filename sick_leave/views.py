from jsonschema import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.models import BaseUserCheck, Branch, SickLeave
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from sick_leave.filters import SickLeaveFilter
from sick_leave.serializers import SickLeaveInputSerializer, SickLeaveListSerializer
from django.db.models import Q
from rest_framework import status
from core.utils import success_response, error_response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

@extend_schema(tags=['Sick Leave'])
class SickLeaveListView(TenantFilterMixin, ListAPIView):
    queryset = SickLeave.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = SickLeaveListSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SickLeaveFilter

@extend_schema(tags=['Sick Leave'])
class SickLeaveRetrieveDestroyView(RetrieveDestroyAPIView, TenantFilterMixin):
    queryset = SickLeave.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = SickLeaveListSerializer
    lookup_field = 'id'

@extend_schema(tags=['Sick Leave'])
class CreateSickLeaveView(CreateAPIView):
    queryset = SickLeave.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = SickLeaveInputSerializer

@extend_schema(tags=['Sick Leave'])
class SickLeaveEditView(UpdateAPIView, TenantFilterMixin):
    queryset = SickLeave.objects.all()
    permission_classes = [IsAuthenticated, HasTenantIdPermission]
    serializer_class = SickLeaveInputSerializer
    lookup_field = 'id'