from rest_framework import serializers

from company.serializers import CompanySerializer
from core.models import Account, Company, EmployeeContract, PaymentType, Salary
from core.serializers import BaseModelInputSerializer
from employee_contract.serializers import EmployeeContractSerializer
from resources.serializers import AccountSerializer, PaymentTypeSerializer

class SalaryListSerializer(serializers.ModelSerializer):
    employee = EmployeeContractSerializer()
    company = CompanySerializer()
    payment_type = PaymentTypeSerializer()
    account = AccountSerializer()

    class Meta:
        model = Salary
        fields = '__all__'

class SalaryInputSerializer(BaseModelInputSerializer):
    date = serializers.DateTimeField(required=True)
    employee = serializers.PrimaryKeyRelatedField(queryset=EmployeeContract.objects.all(), required=True)
    payment_type = serializers.PrimaryKeyRelatedField(queryset=PaymentType.objects.all(), required=True)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=True)

    class Meta:
        model = Salary
        exclude = ('company', 'created_at', 'updated_at', 'created_by', 'updated_by', )