from rest_framework import serializers
from plans.models import OptionCategory, Option, Plan
from drf_extra_fields.fields import HybridImageField
from spaces.models import Space
from utils.mixins import DynamicMixinModelSerializer
from utils.helpers import validate_many_to_many_list
from utils.base64_image_field import Base64ImageField


class OptionCategorySerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)

    class Meta:
        model = OptionCategory
        fields = ("number", "title", "studio", "icon", "slug")
        read_only_fields = ("slug",)


class OptionCategoryUpdateSerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)

    class Meta:
        model = OptionCategory
        fields = "__all__"
        read_only_fields = ("slug", "number", "store",)


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
        read_only_fields = ("slug", "category", "number",)


class PlanSerializer(serializers.ModelSerializer):
    # image_1 = HybridImageField(required=False)
    # image_2 = HybridImageField(required=False)
    # image_3 = HybridImageField(required=False)
    
    image_1 = Base64ImageField(max_length=None, use_url=True, required=False)
    image_2 = Base64ImageField(max_length=None, use_url=True, required=False)
    image_3 = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Plan
        fields = [
            "title", "slug", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)

    # def save(self, validated_data):
    #     space = validated_data.pop('space')
    #     option = validated_data.pop('option')
    #     image_1 = validated_data.pop('image_1')
        
    #     # validate data
    #     validate_many_to_many_list(
    #         value=space, model=Space, fieldName="space", allowBlank=False)
    #     validate_many_to_many_list(
    #         value=option, model=Option, fieldName="option", allowBlank=True)

    #     plan_obj = Plan.objects.create(**validated_data, image_1=image_1)

    #     if plan_obj:
    #         for each_space in space:
    #             plan_obj.space.add(each_space)
    #         for each_option in option:
    #             plan_obj.option.add(each_option)
    #         plan_obj.save()

    #     # return plan object
    #     return plan_obj


class PlanUpdateSerializer(serializers.ModelSerializer):
    # image_1 = HybridImageField(required=False)
    # image_2 = HybridImageField(required=False)
    # image_3 = HybridImageField(required=False)
    
    image_1 = Base64ImageField(max_length=None, use_url=True, required=False)
    image_2 = Base64ImageField(max_length=None, use_url=True, required=False)
    image_3 = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Plan
        fields = [
            "title", "slug", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
        
    
    # def validate(self, data):
    #     print("validate is calling ********", data.get("image_1"))
    #     image_1 = data.pop('image_1')
    #     return data
        
    # def update(self, instance, validated_data):
    #     image_1 = validated_data.pop('image_1', None)
    #     print("uuuuuuuuuuuuuuuuuu")
    #     if image_1:
    #         instance.image_1 = image_1
    #         instance.save()

    #     return super(PlanUpdateSerializer, self).update(instance, validated_data)

    # def update(self, instance, validated_data):
    #     space = validated_data.pop('space')
    #     option = validated_data.pop('option')

    #     # validate data
    #     validate_many_to_many_list(
    #         value=space, model=Space, fieldName="space", allowBlank=False)
    #     validate_many_to_many_list(
    #         value=option, model=Option, fieldName="option", allowBlank=True)

    #     instance = super(PlanUpdateSerializer, self).update(
    #         instance, validated_data)

    #     # clear existing many to many fields
    #     instance.space.clear()
    #     instance.option.clear()

    #     if instance:
    #         for each_space in space:
    #             instance.space.add(each_space)
    #         for each_option in option:
    #             instance.option.add(each_option)
    #         # save instance
    #         instance.save()
    #     # return updated instance
    #     return instance
