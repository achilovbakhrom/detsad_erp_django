from child_contract.serializers import ChildContractSerializer
from core.models import Account, ChildContract, PaymentType, Subscription
from rest_framework import serializers

from core.serializers import BaseModelInputSerializer
from resources.serializers import AccountSerializer, PaymentTypeSerializer

class SubscriptionSerializer(serializers.ModelSerializer):
    child = ChildContractSerializer()
    payment_type = PaymentTypeSerializer()
    account = AccountSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionInputSerializer(BaseModelInputSerializer):
    date = serializers.DateTimeField(required=True)
    child = serializers.PrimaryKeyRelatedField(queryset=ChildContract.objects.all(), required=True)
    payment_type = serializers.PrimaryKeyRelatedField(queryset=PaymentType.objects.all(), required=True)
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=True)

    class Meta:
        model = Subscription
        exclude = ('company', 'created_at', 'updated_at', 'created_by', 'updated_by', )