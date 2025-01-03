from rest_framework.filters import BaseFilterBackend
from django.db.models import Q

class CustomSearchFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search_param = request.query_params.get('search', None)
        print(f'sss {search_param}')
        if search_param:
            return queryset.filter(
                Q(name__icontains=search_param) |
                Q(inn__icontains=search_param)
            )
        
        return queryset