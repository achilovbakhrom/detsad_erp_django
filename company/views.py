from rest_framework import viewsets, permissions
from .serializers import CompanySerializer
from core.models import Company
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Company'])
class CompanyView(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset=Company.objects.all()