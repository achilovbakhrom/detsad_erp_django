from rest_framework import serializers

from branch.serializers import BranchSerializer
from child.serializers import ChildSerializer
from core.models import Branch, ChildContract, Group, GroupRegistration
from core.serializers import BaseModelInputSerializer
from group.serializers import GroupSerializer
from resources.serializers import PaymentTypeSerializer

class GroupRegistrationInputSerializer(BaseModelInputSerializer):
    date = serializers.DateTimeField(required=True)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=True)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)
    children = serializers.PrimaryKeyRelatedField(queryset=ChildContract.objects.all(), many=True, required=False)

    class Meta:
        model = GroupRegistration
        exclude = ('is_deleted', 'company', 'updated_by', 'created_by', 'created_at', 'updated_at',)

    def create(self, validated_data):
        children = validated_data.pop('children', [])
        group_registration = super().create(validated_data)
        for child in children:
            child_contract = ChildContract.objects.get(id=child.id)
            child_contract.group_registration_id = group_registration.id
            child_contract.status = 'created'
            child_contract.save()
        return group_registration

class ChildContractGroupSerializer(serializers.ModelSerializer):
    child = ChildSerializer()
    payment_type = PaymentTypeSerializer()
    class Meta:
        model = ChildContract
        fields = '__all__'

class GroupRegistrationListSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    branch = BranchSerializer()
    child_contracts = ChildContractGroupSerializer(many=True, read_only=True, source='childcontract_set')

    class Meta:
        model = GroupRegistration
        fields = '__all__'

class GroupRegistrationUpdateStatusSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)