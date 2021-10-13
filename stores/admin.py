from django.contrib import admin
from .models import Store, CustomBusinessDay
from utils.mixins import CustomModelAdminMixin


class StoreAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Store

admin.site.register(Store, StoreAdmin)

class CustomBusinessDayAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = CustomBusinessDay

admin.site.register(CustomBusinessDay, CustomBusinessDayAdmin)
