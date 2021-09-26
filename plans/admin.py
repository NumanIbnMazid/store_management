from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import OptionCategory, Option, Plan


class OptionCategoryAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = OptionCategory
        

admin.site.register(OptionCategory, OptionCategoryAdmin)


class OptionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Option
admin.site.register(Option, OptionAdmin)


class PlanAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = Plan
admin.site.register(Plan, PlanAdmin)