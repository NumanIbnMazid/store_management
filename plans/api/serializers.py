from rest_framework import serializers
from plans.models import OptionCategory, Option, Plan
from drf_extra_fields.fields import HybridImageField

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

class PlanSerializer(serializers.ModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ("slug",)

class PlanUpdateSerializer(serializers.ModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ("slug", "space", "option")
