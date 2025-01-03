from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .base import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display=['id', 'name', 'username', 'role', 'is_active', 'is_staff', 'last_login']
    list_editable=['name', 'username', 'role', 'is_active']
    list_display_links = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2',
                'role',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )
