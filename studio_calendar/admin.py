from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import StudioCalendar, BusinessDay, BusinessHour


class StudioCalendarAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = StudioCalendar


admin.site.register(StudioCalendar, StudioCalendarAdmin)

class BusinessDayAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = BusinessDay


admin.site.register(BusinessDay, BusinessDayAdmin)

class BusinessHourAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = BusinessHour


admin.site.register(BusinessHour, BusinessHourAdmin)
