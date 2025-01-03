
from core.models import Branch, Company
from rest_framework import serializers

class BranchSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())
    class Meta:
        model = Branch
        fields = '__all__'
    
    