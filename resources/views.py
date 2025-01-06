from rest_framework import viewsets

from core.models import Department, PaymentType, Position, Reason
from core.pagination import CustomPagination
from resources.serializers import DepartmentSerializer, PaymentTypeSerializer, PositionSerializer, ReasonSerializer
from rest_framework import permissions
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Resources'])
class BaseResourceView(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated]
    
    class Meta:
        abstract = True

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(exclude=True)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    

class PositionView(BaseResourceView):
    serializer_class = PositionSerializer
    queryset = Position.objects.filter(is_deleted=False)

class ReasonView(BaseResourceView):
    serializer_class = ReasonSerializer
    queryset = Reason.objects.filter(is_deleted=False)

class DepartmentView(BaseResourceView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.filter(is_deleted=False)

class PaymentTypeView(BaseResourceView):
    serializer_class = PaymentTypeSerializer
    queryset = PaymentType.objects.filter(is_deleted=False)

    