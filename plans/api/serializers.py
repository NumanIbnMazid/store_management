from plans.models import OptionCategory, Option, Plan
from drf_extra_fields.fields import HybridImageField
from utils.mixins import DynamicMixinModelSerializer
from utils.helpers import ResponseWrapper
from rest_framework import serializers


class OptionCategorySerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)
    
    class Meta:
        model = OptionCategory
        fields = ("number", "title", "studio", "icon",)
        read_only_fields = ("slug",)
        

class OptionCategoryUpdateSerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)
    
    class Meta:
        model = OptionCategory
        fields = "__all__"
        read_only_fields = ("slug","number", "store",)
        

class OptionSerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug",)


class OptionUpdateSerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)
    
    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug","category","number",)
        

class PlanSerializer(DynamicMixinModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    # space = serializers.PrimaryKeyRelatedField(many=True, queryset=Space.objects.all())
    
    class Meta:
        model = Plan
        fields = [
            "title", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
    
    def save(self, validated_data):
        try:
            space = validated_data.pop('space')
            option = validated_data.pop('option')
            plan_obj = Plan.objects.create(**validated_data)
            if plan_obj:
                for each_space in space:
                    plan_obj.space.add(each_space)
                for each_option in option:
                    plan_obj.option.add(each_option)
                plan_obj.save()
                return plan_obj
            serializer = PlanSerializer(data=plan_obj)
            if serializer.errors:
                raise serializers.ValidationError(serializer.errors)
            return ResponseWrapper(data=serializer.data, status=200)
        
        except AttributeError as E:
            raise serializers.ValidationError(str(E))

class PlanUpdateSerializer(DynamicMixinModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Plan
        fields = [
            "title", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
    
    def update_plan(self, validated_data, instance):
        try:
            print("______vd__f___", instance.id)
            space = validated_data.pop('space')
            option = validated_data.pop('option')
            plan_obj = Plan.objects.update_or_create(**validated_data)
            if plan_obj:
                for each_space in space:
                    plan_obj.space.add(each_space)
                    plan_obj.id.add(instance.id)
                for each_option in option:
                    plan_obj.option.add(each_option)
                    
                plan_obj.save()
                return plan_obj
            serializer = PlanSerializer(data=plan_obj)
            if serializer.errors:
                raise serializers.ValidationError(serializer.errors)
            return ResponseWrapper(data=serializer.data, status=200)

        except AttributeError as E:
            raise serializers.ValidationError(str(E))
