from rest_framework import serializers
from plans.models import OptionCategory, Option, Plan


class OptionCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OptionCategory
        fields = "__all__"
        read_only_fields = ("slug",)


class OptionCategoryUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OptionCategory
        fields = "__all__"
        read_only_fields = ("slug","number", "store",)



class OptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug",)

class OptionUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug","category","number",)


class PlanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ("slug",)

class PlanUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Plan
        fields = "__all__"
        read_only_fields = ("slug", "space", "option")
