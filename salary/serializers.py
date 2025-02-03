from rest_framework import serializers

from company.serializers import CompanySerializer
from core.models import Company, EmployeeContract, Salary
from employee_contract.serializers import EmployeeContractSerializer

class SalaryListSerializer(serializers.ModelSerializer):
    employee = EmployeeContractSerializer()
    company = CompanySerializer()

    class Meta:
        model = Salary
        fields = '__all__'

class CreateSalarySerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    employee = serializers.PrimaryKeyRelatedField(queryset=EmployeeContract.objects.all(), required=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True)

    class Meta:
        model = Salary
        fields = '__all__'