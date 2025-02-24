from rest_framework import serializers

from core.models import BaseUserCheck, Company
from core.permissions import get_tenant_id

class AuditSerializerMixin(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def create(self, validated_data):
        request = self.context.get('request', None)
        instance = self.Meta.model(**validated_data)
        instance.save(request=request)

        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save(request=request)

        return instance

    def delete(self, instance):
        request = self.context.get('request', None)

        instance.delete(request=request)

    def to_internal_value(self, data):
        category_id = data.get('id', None)
        validated_data = super().to_internal_value(data)
        if category_id is not None:
            validated_data['id'] = category_id

        return validated_data
    

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