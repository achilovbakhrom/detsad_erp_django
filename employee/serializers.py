from core.models import Employee, Company
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Employee
        fields = '__all__'