import django_filters

from core.models import Child

class ChildFilterSet(django_filters.FilterSet):
    date_of_birth = django_filters.DateFilter(field_name='date_of_birth')

    class Meta:
        model = Child
        fields = ['date_of_birth']