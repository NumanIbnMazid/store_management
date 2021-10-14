from rest_framework import serializers
from plans.models import OptionCategory, Option, Plan
from drf_extra_fields.fields import HybridImageField
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class OptionCategorySerializer(serializers.ModelSerializer):
    icon = HybridImageField(required=False)
    
    class Meta:
        model = OptionCategory
        fields = ("number", "title", "studio", "icon",)
        read_only_fields = ("slug",)
        
class OptionCategoryUpdateSerializer(serializers.ModelSerializer):
    icon = HybridImageField(required=False)
    
    class Meta:
        model = OptionCategory
        fields = "__all__"
        read_only_fields = ("slug","number", "store",)
        
    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = OptionCategory.objects.get(**self.initial_data)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return super().is_valid(raise_exception)
            else:
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            return super().is_valid(raise_exception)


class OptionSerializer(serializers.ModelSerializer):
    icon = HybridImageField(required=False)
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug",)

class OptionUpdateSerializer(serializers.ModelSerializer):
    icon = HybridImageField(required=False)
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug","category","number",)
        
    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = Option.objects.get(**self.initial_data)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return super().is_valid(raise_exception)
            else:
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            return super().is_valid(raise_exception)

class PlanSerializer(serializers.ModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Plan
        fields = [
            "title", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
        
class PlanUpdateSerializer(serializers.ModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Plan
        fields = [
            "title", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
        
    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = Plan.objects.get(**self.initial_data)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return super().is_valid(raise_exception)
            else:
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            return super().is_valid(raise_exception)
