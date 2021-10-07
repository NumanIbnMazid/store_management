from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import Notification


class NotificationAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = Notification
        
admin.site.register(Notification, NotificationAdmin)