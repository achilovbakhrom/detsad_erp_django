from company.serializers import CompanySerializer
from core.models import Child
from rest_framework import serializers

from core.serializers import BaseModelInputSerializer


class ChildSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Child
        fields = '__all__'

class ChildInputSerializer(BaseModelInputSerializer):
    class Meta:
        model = Child
        fields = '__all__'