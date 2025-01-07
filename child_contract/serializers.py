from rest_framework import serializers

from child.serializers import ChildSerializer
from core.models import Child, ChildContract, GroupRegistration, PaymentType
from group_registration.serializers import GroupRegistrationListSerializer
from resources.serializers import PaymentTypeSerializer

class CreateChildContractSerializer(serializers.ModelSerializer):
    child = serializers.PrimaryKeyRelatedField(queryset = Child.objects.all(), required=True)
    payment_type = serializers.PrimaryKeyRelatedField(queryset = PaymentType.objects.all(), required=True)
    group_registration = serializers.PrimaryKeyRelatedField(queryset = GroupRegistration.objects.all())
    
    class Meta:
        model = ChildContract
        fields = '__all__'

class ChildContractSerializer(serializers.ModelSerializer):
    child = ChildSerializer()
    payment_type = PaymentTypeSerializer()
    group_registration = GroupRegistrationListSerializer()
    class Meta:
        model = ChildContract
        fields = '__all__'
