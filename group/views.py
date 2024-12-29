from rest_framework import viewsets, permissions
from .serializers import GroupSerializer
from core.models import Company
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Group'])
class GroupView(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset=Company.objects.all()