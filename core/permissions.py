from rest_framework.permissions import BasePermission

from core.models import CompanyUserRelation
from .exceptions import TenantAccessDenied, TenantIDRequired


TENANT_ID = 'X-Tenant-ID'

def get_tenant_id(request):
    return request.headers.get(TENANT_ID)

def company_belongs_to_user(user_id, company_id):
    if company_id is None:
        return (False, "The 'company_id' is a required parameter")
    
    companies = CompanyUserRelation.objects.filter(user_id=user_id, company_id=company_id)

    if len(companies) == 0:
        return (False, "'company_id' is not found for given 'user_id'")
    
    return (True, None)

class HasTenantIdPermission(BasePermission):
    """
    Allows access only if Tenant-ID is provided in the request headers.
    """

    def has_permission(self, request, view):
        company_id = get_tenant_id(request)
        if company_id is None:
            raise TenantIDRequired()
        
        user_id = request.user.id

        request.tenant_id = company_id

        (belongs, _) = company_belongs_to_user(user_id, company_id)
        if not belongs:
            raise TenantAccessDenied()

        return True
