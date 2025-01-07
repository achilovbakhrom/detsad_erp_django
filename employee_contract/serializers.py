from rest_framework import serializers

from branch.serializers import BranchSerializer
from core.models import Branch, Department, Employee, EmployeeContract, Position
from employee.serializers import EmployeeSerializer
from resources.serializers import DepartmentSerializer, PositionSerializer

class EmployeeContractSerializer(serializers.ModelSerializer):
    
    employee = EmployeeSerializer()
    position = PositionSerializer()
    department = DepartmentSerializer()
    branch = BranchSerializer()
    
    class Meta:
        model = EmployeeContract
        fields = '__all__'

class CreateEmployeeContractSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=True)
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all(), required=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=True)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)
    salary = serializers.DecimalField(required=True, decimal_places=2, max_digits=15)

    class Meta:
        model = EmployeeContract
        fields = '__all__'