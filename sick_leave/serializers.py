from rest_framework import serializers

from child_contract.serializers import ChildContractSerializer
from company.serializers import CompanySerializer
from core.models import ChildContract, Company, SickLeave
from core.serializers import BaseModelInputSerializer

class SickLeaveListSerializer(serializers.ModelSerializer):
    child = ChildContractSerializer()
    company = CompanySerializer()

    class Meta:
        model = SickLeave
        fields = '__all__'

class SickLeaveInputSerializer(BaseModelInputSerializer):
    date = serializers.DateTimeField(required=True)
    child = serializers.PrimaryKeyRelatedField(queryset=ChildContract.objects.all(), required=True)

    class Meta:
        model = SickLeave
        exclude = ('company', 'updated_by', 'created_by', 'created_at', 'updated_at',)