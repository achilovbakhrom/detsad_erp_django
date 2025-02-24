from rest_framework import serializers

from core.models import BaseUserCheck, Company
from core.permissions import get_tenant_id


class BaseModelInputSerializer(serializers.ModelSerializer, BaseUserCheck):
    
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