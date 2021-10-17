from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'slug', 'name', 'is_customer', 'is_studio_admin', 'is_store_staff', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('id', 'email', 'username', 'slug', 'name', 'is_customer', 'is_studio_admin', 'is_store_staff', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_studio_admin', 'is_store_staff', 'is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'username', 'contact_number')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
