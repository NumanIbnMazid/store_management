from django.contrib import admin
from .models import Studio, StudioModerator
from utils.mixins import CustomModelAdminMixin


class StudioAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = Studio


admin.site.register(Studio, StudioAdmin)

class StudioModeratorAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = StudioModerator


admin.site.register(StudioModerator, StudioModeratorAdmin)
