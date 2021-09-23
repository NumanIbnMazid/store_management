from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.get_fields()]

    class Meta:
        model = Customer


admin.site.register(Customer, CustomerAdmin)
