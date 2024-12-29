from rest_framework import viewsets, permissions
from .serializers import ChildSerializer
from core.models import Child
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Children'])
class ChildView(viewsets.ModelViewSet):
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset=Child.objects.all()