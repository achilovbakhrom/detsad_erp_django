from rest_framework import serializers

from company.serializers import CompanySerializer
from core.models import Account, BaseUserCheck, Company, Department, PaymentType, Position, Reason
from core.permissions import get_tenant_id

class BaseResourceModelInputSerializer(serializers.ModelSerializer, BaseUserCheck):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        abstract = True

    def create(self, validated_data):
        request = self.context.get('request')
        tenant_id = get_tenant_id(request)
        validated_data['company'] = Company.objects.get(id=tenant_id)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        tenant_id = get_tenant_id(request)
        company_id = validated_data.get('company').id
        if self.company_belongs_to_user(user_id, company_id):
            validated_data['company'] = Company.objects.get(id=tenant_id)
        return super().update(instance, validated_data)

class PositionSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Position
        fields = '__all__'

class PositionInputSerializer(BaseResourceModelInputSerializer):
    class Meta:
        model = Position
        fields = '__all__'
    

class ReasonSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Reason
        fields = '__all__'

class ReasonInputSerializer(BaseResourceModelInputSerializer):
    class Meta:
        model = Reason
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentInputSerializer(BaseResourceModelInputSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class PaymentTypeSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = PaymentType
        fields = '__all__'

class PaymentTypeInputSerializer(BaseResourceModelInputSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Account
        fields = '__all__'

class AccountInputSerializer(BaseResourceModelInputSerializer):
    class Meta:
        model = Account
        fields = '__all__'