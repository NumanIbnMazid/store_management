from django.contrib import admin
from utils.mixins import CustomModelAdminMixin
from .models import Category, Option, Time, Product


class CategoryAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Category
        
admin.site.register(Category, CategoryAdmin)


class OptionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass

    class Meta:
        model = Option
admin.site.register(Option, OptionAdmin)


class ProductAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = Product
admin.site.register(Product, ProductAdmin)


class TimeAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
    class Meta:
        model = Time
admin.site.register(Time, TimeAdmin)