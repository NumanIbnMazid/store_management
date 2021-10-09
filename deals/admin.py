from django.contrib import admin
from .models import Coupon
from utils.mixins import CustomModelAdminMixin


class CouponAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Coupon


admin.site.register(Coupon, CouponAdmin)
