from plans.models import OptionCategory, Option, Plan
from drf_extra_fields.fields import HybridImageField
from spaces.models import Space
from utils.mixins import DynamicMixinModelSerializer
from utils.helpers import validate_many_to_many_list


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
    
    class Meta:
        model = Plan
        fields = [
            "title", "slug", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
    
    def save(self, validated_data):
        space = validated_data.pop('space')
        option = validated_data.pop('option')
        
        # validate data
        validate_many_to_many_list(value=space, model=Space, fieldName="space", allowBlank=False)
        validate_many_to_many_list(value=option, model=Option, fieldName="option", allowBlank=True)
        
        plan_obj = Plan.objects.create(**validated_data)
        
        if plan_obj:
            for each_space in space:
                plan_obj.space.add(each_space)
            for each_option in option:
                plan_obj.option.add(each_option)
            plan_obj.save()
            
        # return plan object
        return plan_obj

class PlanUpdateSerializer(DynamicMixinModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Plan
        fields = [
            "title", "slug", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
        
        
    def update(self, instance, validated_data):
        space = validated_data.pop('space')
        option = validated_data.pop('option')
        
        # validate data
        validate_many_to_many_list(value=space, model=Space, fieldName="space", allowBlank=False)
        validate_many_to_many_list(value=option, model=Option, fieldName="option", allowBlank=True)
        
        instance = super(PlanUpdateSerializer, self).update(instance, validated_data)
        
        # clear existing many to many fields
        instance.space.clear()
        instance.option.clear()
        
        if instance:
            for each_space in space:
                instance.space.add(each_space)
            for each_option in option:
                instance.option.add(each_option)
            # save instance
            instance.save()
        # return updated instance
        return instance
