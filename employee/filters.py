import django_filters

from core.models import Employee

class EmployeeFilterSet(django_filters.FilterSet):
    date_of_birth = django_filters.DateFilter(field_name='date_of_birth')

    class Meta:
        model = Employee
        fields = ['date_of_birth']