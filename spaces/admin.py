from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import Space


class SpaceAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Space
        
admin.site.register(Space, SpaceAdmin)