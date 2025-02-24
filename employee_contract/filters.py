import django_filters
from core.models import EmployeeContract

class EmployeeContractFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    salary_from = django_filters.NumberFilter(field_name="salary", lookup_expr='gte')
    salary_to = django_filters.NumberFilter(field_name="salary", lookup_expr='lte')

    class Meta:
        model = EmployeeContract
        fields = ['branch_id', 'status', 'employee_id', 'position_id', 'department_id', 'salary_from', 'salary_to', 'date_from', 'date_to']
