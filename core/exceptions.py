from rest_framework.exceptions import APIException

class TenantIDRequired(APIException):
    status_code = 400
    default_detail = "Tenant-ID header is required."
    default_code = "tenant_id_required"

class TenantAccessDenied(APIException):
    status_code = 403
    default_detail = "You do not have access to this Tenant-ID."
    default_code = "tenant_access_denied"