from child_contract.serializers import ChildContractSerializer
from core.models import Subscription
from rest_framework import serializers

from resources.serializers import AccountSerializer, PaymentTypeSerializer

class SubscriptionSerializer(serializers.ModelSerializer):
    child = ChildContractSerializer()
    payment_type = PaymentTypeSerializer()
    account = AccountSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionInputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    child = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all(), required=True)
    payment_type = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all(), required=True)
    account = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all(), required=True)

    class Meta:
        model = Subscription
        fields = '__all__'