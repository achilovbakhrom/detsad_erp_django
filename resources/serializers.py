from rest_framework import serializers

from core.models import Department, PaymentType, Position, Reason

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'