from rest_framework import serializers
from core.models import BaseUserCheck, Company

class BaseModelInputSerializer(serializers.ModelSerializer, BaseUserCheck):
    
    class Meta:
        abstract = True

    def create(self, validated_data):
        request = self.context.get('request')
        if request is None:
            raise ValueError("Request is not available in the context.")
        tenant_id = request.tenant_id
        validated_data['company'] = Company.objects.get(id=tenant_id)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request is None:
            raise ValueError("Request is not available in the context.")
        user_id = request.user.id
        tenant_id = request.tenant_id
        validated_data['company'] = Company.objects.get(id=tenant_id)
        if self.company_belongs_to_user(user_id, tenant_id):
            validated_data['company'] = Company.objects.get(id=tenant_id)
        return super().update(instance, validated_data)