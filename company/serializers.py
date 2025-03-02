from core.models import Company
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    is_default = serializers.BooleanField(required=True)
    name = serializers.CharField(required=True)
    class Meta:
        model = Company
        exclude = ('is_deleted', )