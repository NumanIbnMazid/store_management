from django.contrib import admin
from .models import Store, CustomBusinessDay, StoreModerator
from utils.mixins import CustomModelAdminMixin


class StoreAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Store

admin.site.register(Store, StoreAdmin)

class StoreModeratorAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = StoreModerator


admin.site.register(StoreModerator, StoreModeratorAdmin)

class CustomBusinessDayAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = CustomBusinessDay

admin.site.register(CustomBusinessDay, CustomBusinessDayAdmin)
