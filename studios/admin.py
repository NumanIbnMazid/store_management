from django.contrib import admin
from .models import Studio, VatTax, Currency
from utils.mixins import CustomModelAdminMixin


class StudioAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = Studio


admin.site.register(Studio, StudioAdmin)


class VatTaxAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = VatTax


admin.site.register(VatTax, VatTaxAdmin)


class CurrencyAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = Currency


admin.site.register(Currency, CurrencyAdmin)
