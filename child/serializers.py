from core.models import Child, Company
from rest_framework import serializers


class ChildSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = Child
        fields = '__all__'