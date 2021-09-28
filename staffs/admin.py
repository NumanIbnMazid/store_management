from django.contrib import admin
from .models import Staff


class StaffAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Staff._meta.get_fields()]

    class Meta:
        model = Staff


admin.site.register(Staff, StaffAdmin)