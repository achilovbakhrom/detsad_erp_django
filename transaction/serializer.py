from rest_framework import serializers

from child_contract.serializers import ChildContractSerializer
from company.serializers import CompanySerializer
from core.models import Account, ChildContract, Company, PaymentType, Transaction
from resources.serializers import AccountSerializer, PaymentTypeSerializer

class TransactionSerializer(serializers.ModelSerializer):
    child = ChildContractSerializer()
    company = CompanySerializer()
    payment_type = PaymentTypeSerializer()
    account = AccountSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'


class CreateTransactionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    child = serializers.PrimaryKeyRelatedField(queryset=ChildContract.objects.all(), required=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True)
    payment_type = serializers.PrimaryKeyRelatedField(queryset=PaymentType.objects.all(), required=True)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=True)

    class Meta:
        model = Transaction
        fields = '__all__'