from company.serializers import CompanySerializer
from core.models import Group
from rest_framework import serializers

from core.serializers import BaseModelInputSerializer


class GroupSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Group
        fields = '__all__'

class GroupInputSerializer(BaseModelInputSerializer):
    class Meta:
        model = Group
        fields = '__all__'
