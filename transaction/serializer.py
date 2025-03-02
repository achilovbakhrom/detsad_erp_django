from rest_framework import serializers

from child_contract.serializers import ChildContractSerializer
from company.serializers import CompanySerializer
from core.models import Account, ChildContract, Company, PaymentType, Reason, Transaction
from core.serializers import BaseModelInputSerializer
from resources.serializers import AccountSerializer, PaymentTypeSerializer

class TransactionSerializer(serializers.ModelSerializer):
    child = ChildContractSerializer()
    company = CompanySerializer()
    payment_type = PaymentTypeSerializer()
    account = AccountSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionInputSerializer(BaseModelInputSerializer):
    date = serializers.DateTimeField(required=True)
    child = serializers.PrimaryKeyRelatedField(queryset=ChildContract.objects.all(), required=False)
    payment_type = serializers.PrimaryKeyRelatedField(queryset=PaymentType.objects.all(), required=True)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=True)
    reason = serializers.PrimaryKeyRelatedField(queryset=Reason.objects.all(), required=False)

    class Meta:
        model = Transaction
        exclude = ('company', 'created_at', 'updated_at', 'created_by', 'updated_by', )