from django.contrib import admin
from .models import Coupon, PointSetting, EarlyBirdDiscount, PeriodicalDiscount
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

class EarlyBirdDiscountAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = EarlyBirdDiscount
admin.site.register(EarlyBirdDiscount, EarlyBirdDiscountAdmin)

class PeriodicalDiscountAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = PeriodicalDiscount
admin.site.register(PeriodicalDiscount, PeriodicalDiscountAdmin)
