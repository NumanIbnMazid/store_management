from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import StudioCalendar


class StudioCalendarAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = StudioCalendar


admin.site.register(StudioCalendar, StudioCalendarAdmin)
