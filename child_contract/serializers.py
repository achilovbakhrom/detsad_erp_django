from rest_framework import serializers

from child.serializers import ChildSerializer
from core.models import Branch, Child, ChildContract, GroupRegistration, PaymentType
from core.serializers import BaseModelInputSerializer
from group_registration.serializers import GroupRegistrationListSerializer
from resources.serializers import PaymentTypeSerializer

class ChildContractInputSerializer(BaseModelInputSerializer):
    child = serializers.PrimaryKeyRelatedField(queryset = Child.objects.all(), required=True)
    payment_type = serializers.PrimaryKeyRelatedField(queryset = PaymentType.objects.all(), required=True)
    group_registration = serializers.PrimaryKeyRelatedField(queryset = GroupRegistration.objects.all(), required=False)
    branch = serializers.PrimaryKeyRelatedField(queryset = Branch.objects.all(), required=True)
    class Meta:
        model = ChildContract
        exclude = ('is_deleted', 'company', 'updated_by', 'created_by', 'created_at', 'updated_at',)

class ChildContractSerializer(serializers.ModelSerializer):
    child = ChildSerializer()
    payment_type = PaymentTypeSerializer()
    group_registration = GroupRegistrationListSerializer()
    class Meta:
        model = ChildContract
        fields = '__all__'

class ChangeStatusSelrializer(serializers.Serializer):
    status = serializers.CharField(required=True)
