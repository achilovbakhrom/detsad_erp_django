from rest_framework import serializers

from company.serializers import CompanySerializer
from core.models import Account, Department, PaymentType, Position, Reason
from core.serializers import BaseModelInputSerializer

class PositionSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Position
        fields = '__all__'

class PositionInputSerializer(BaseModelInputSerializer):
    class Meta:
        model = Position
        exclude = ('company', 'is_deleted')
    

class ReasonSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Reason
        fields = '__all__'

class ReasonInputSerializer(BaseModelInputSerializer):
    class Meta:
        model = Reason
        exclude = ('company', 'is_deleted')

class DepartmentSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentInputSerializer(BaseModelInputSerializer):
    class Meta:
        model = Department
        exclude = ('company', 'is_deleted')

class PaymentTypeSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = PaymentType
        fields = '__all__'

class PaymentTypeInputSerializer(BaseModelInputSerializer):
    class Meta:
        model = PaymentType
        exclude = ('company', 'is_deleted')

class AccountSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Account
        fields = '__all__'

class AccountInputSerializer(BaseModelInputSerializer):
    class Meta:
        model = Account
        exclude = ('company', 'is_deleted', 'created_by', 'updated_by', )