from core.permissions import get_tenant_id


class NonDeletedFilterMixin:

    class Meta:
        abstract = True

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(queryset, 'active'):
            return queryset.active()

        return queryset.filter(is_deleted=False)

class TenantFilterMixin:
    class Meta:
        abstract = True
    
    def get_queryset(self):

        queryset = super().get_queryset()
        if hasattr(queryset, 'active'):
            return queryset.active()
        
        company_id = get_tenant_id(self.request)

        return queryset.filter(company_id=company_id)