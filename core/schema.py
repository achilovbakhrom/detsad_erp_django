# schemas.py
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiParameter

class TenantHeaderAutoSchema(AutoSchema):
    """
    Automatically adds X-TENANT-ID header to all endpoints in Swagger.
    """
    target_permission = 'core.permissions.HasTenantIdPermission'

    def get_override_parameters(self):
        view = self.view
        # Check if the view has the target permission
        if any(
            perm for perm in getattr(view, 'permission_classes', []) 
            if perm.__module__ + '.' + perm.__name__ == self.target_permission
        ):
            
            tenant_param = OpenApiParameter(
                name="X-TENANT-ID",
                type=str,
                location=OpenApiParameter.HEADER,
                required=False,
                description="Tenant ID (for multi-tenant requests)",
            )
            return [tenant_param] + super().get_override_parameters()

        return super().get_override_parameters()
