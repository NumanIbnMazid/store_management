from django.contrib import admin
from .models import Store
from utils.mixins import CustomModelAdminMixin


class StoreAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Store

admin.site.register(Store, StoreAdmin)
