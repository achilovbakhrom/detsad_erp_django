from core.models import Company, Group
from rest_framework import serializers


class GroupSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = Group
        fields = '__all__'