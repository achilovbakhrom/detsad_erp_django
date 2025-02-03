from rest_framework import serializers
from child_contract.serializers import ChildContractSerializer
from resources.serializers import PaymentTypeSerializer, ReasonSerializer
from company.serializers import CompanySerializer
from core.models import Cashbox, PaymentType, Reason, Company

class CashboxSerializer(serializers.ModelSerializer):
    payment_type=PaymentTypeSerializer()
    reason=ReasonSerializer()
    company=CompanySerializer()
    child=ChildContractSerializer()

    class Meta:
        model=Cashbox
        fields = '__all__'
    
class CreateCashboxSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    payment_type = serializers.PrimaryKeyRelatedField(queryset=PaymentType.objects.all(), required=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True)

    class Meta:
        model=Cashbox
        fields = '__all__'