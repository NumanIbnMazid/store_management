from rest_framework import serializers
from plans.models import OptionCategory, Option, Plan
from utils.base64_image import Base64ImageField

class OptionCategorySerializer(serializers.ModelSerializer):
    icon = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = OptionCategory
        fields = ("number", "title", "studio", "icon",)
        read_only_fields = ("slug",)


class OptionCategoryUpdateSerializer(serializers.ModelSerializer):
    icon = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = OptionCategory
        fields = "__all__"
        read_only_fields = ("slug","number", "store",)


class OptionSerializer(serializers.ModelSerializer):
    icon = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug",)

class OptionUpdateSerializer(serializers.ModelSerializer):
    icon = Base64ImageField(max_length=None, use_url=True)
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug","category","number",)

class PlanSerializer(serializers.ModelSerializer):
    image_1 = Base64ImageField(max_length=None, use_url=True)
    image_2 = Base64ImageField(max_length=None, use_url=True)
    image_3 = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ("slug",)

class PlanUpdateSerializer(serializers.ModelSerializer):
    image_1 = Base64ImageField(max_length=None, use_url=True)
    image_2 = Base64ImageField(max_length=None, use_url=True)
    image_3 = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ("slug", "space", "option")
