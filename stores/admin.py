from django.contrib import admin
from .models import Store, CustomClosedDay
from utils.mixins import CustomModelAdminMixin


class StoreAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Store

admin.site.register(Store, StoreAdmin)

class CustomClosedDayAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = CustomClosedDay

admin.site.register(CustomClosedDay, CustomClosedDayAdmin)
