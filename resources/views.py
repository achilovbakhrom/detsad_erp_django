from requests import Response
from rest_framework import viewsets

from core.mixins import NonDeletedFilterMixin, TenantFilterMixin
from core.models import Account, Department, PaymentType, Position, Reason
from core.pagination import CustomPagination
from core.permissions import HasTenantIdPermission
from resources.serializers import AccountInputSerializer, AccountSerializer, DepartmentInputSerializer, DepartmentSerializer, PaymentTypeInputSerializer, PaymentTypeSerializer, PositionInputSerializer, PositionSerializer, ReasonInputSerializer, ReasonSerializer
from rest_framework import permissions
from drf_spectacular.utils import extend_schema
from rest_framework import status

@extend_schema(tags=['Resources'])
class BaseResourceView(NonDeletedFilterMixin, TenantFilterMixin, viewsets.ModelViewSet):
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, HasTenantIdPermission]
    http_method_names = ['get', 'post', 'delete', 'put']    
    class Meta:
        abstract = True

    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return Response({"detail": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PositionView(BaseResourceView):
    queryset = Position.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return PositionInputSerializer
        return PositionSerializer

class ReasonView(BaseResourceView):
    queryset = Reason.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return ReasonInputSerializer
        return ReasonSerializer

class DepartmentView(BaseResourceView):
    queryset = Department.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return DepartmentInputSerializer
        return DepartmentSerializer

class PaymentTypeView(BaseResourceView):
    queryset = PaymentType.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return PaymentTypeInputSerializer
        return PaymentTypeSerializer

class AccountView(BaseResourceView):
    queryset = Account.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return AccountInputSerializer
        return AccountSerializer

    