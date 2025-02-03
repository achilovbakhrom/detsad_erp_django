from rest_framework import serializers

from child_contract.serializers import ChildContractSerializer
from company.serializers import CompanySerializer
from core.models import ChildContract, Company, SickLeave

class SickLeaveListSerializer(serializers.ModelSerializer):
    child = ChildContractSerializer()
    company = CompanySerializer()

    class Meta:
        model = SickLeave
        fields = '__all__'

class CreateSickLeaveSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    child = serializers.PrimaryKeyRelatedField(queryset=ChildContract.objects.all(), required=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True)

    class Meta:
        model = SickLeave
        fields = '__all__'