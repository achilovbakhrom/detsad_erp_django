
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
        
        print(self.request.tenant_id)
        
        return queryset.filter(company_id=self.request.tenant_id)