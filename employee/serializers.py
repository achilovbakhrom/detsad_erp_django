from company.serializers import CompanySerializer
from core.models import Employee, Company
from rest_framework import serializers

from core.serializers import BaseModelInputSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeInputSerializer(BaseModelInputSerializer):
    class Meta:
        model = Employee
        exclude = ('company', 'is_deleted', )