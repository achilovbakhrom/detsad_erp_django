from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .serializers import BranchSerializer
from core.models import Branch
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Branch'])
class BranchView(viewsets.ModelViewSet):
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset=Branch.objects.all()