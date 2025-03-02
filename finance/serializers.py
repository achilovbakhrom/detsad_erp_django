from rest_framework import serializers

from resources.serializers import AccountSerializer, PaymentTypeSerializer

class BalanceSerializer(serializers.Serializer):
    account = AccountSerializer()
    payment_type = PaymentTypeSerializer()
    balance = serializers.DecimalField(decimal_places=2, max_digits=15)

class TransactionSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    account = AccountSerializer()
    payment_type = PaymentTypeSerializer()
    amount = serializers.DecimalField(decimal_places=2, max_digits=15)
    tx_type = serializers.CharField()
    entity_id = serializers.IntegerField()

class AcountFinanceReportSerializer(serializers.Serializer):
    balance = BalanceSerializer(many=True)
    transactions = TransactionSerializer(many=True)