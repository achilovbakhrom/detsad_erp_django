from core.models import Branch
from rest_framework import serializers
from company.serializers import CompanySerializer
from core.serializers import BaseModelInputSerializer

class BranchSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    class Meta:
        model = Branch
        fields = '__all__'
        
    
class BranchInputSerializer(BaseModelInputSerializer):
    class Meta(BaseModelInputSerializer.Meta):
        model = Branch
        exclude = ('company', 'is_deleted', )
        