from django.contrib import admin
from .models import Coupon, PointSetting
from utils.mixins import CustomModelAdminMixin


class CouponAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Coupon
admin.site.register(Coupon, CouponAdmin)



class PointSettingAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = PointSetting
admin.site.register(PointSetting, PointSettingAdmin)
