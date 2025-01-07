from rest_framework import serializers

from branch.serializers import BranchSerializer
from core.models import Branch, ChildContract, Group, GroupRegistration
from group.serializers import GroupSerializer

class CreateGroupRegistrationSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=True)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)

    class Meta:
        model = GroupRegistration
        fields = '__all__'

class CreateGroupRegistrationDTO(CreateGroupRegistrationSerializer):
    children = serializers.PrimaryKeyRelatedField(queryset=ChildContract.objects.all(), many=True)

class GroupRegistrationListSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    branch = BranchSerializer()

    class Meta:
        model = GroupRegistration
        fields = '__all__'

class GroupRegistrationUpdateStatusSerializer(serializers.Serializer):
    status = serializers.CharField(required=True)