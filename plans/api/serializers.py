from rest_framework import serializers
from plans.models import OptionCategory, Option, Plan
from drf_extra_fields.fields import HybridImageField
from utils.mixins import DynamicMixinModelSerializer
from drf_extra_fields.fields import HybridImageField
from utils.helpers import get_file_representations
from studios.api.serializers import StudioShortInfoSerializer
from spaces.api.serializers import SpaceShortInfoSerializer


class OptionCategoryShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionCategory
        fields = ["id", "number", "title", "slug"]
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(OptionCategoryShortInfoSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation


class OptionCategorySerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)

    class Meta:
        model = OptionCategory
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(OptionCategorySerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        representation = get_file_representations(representation=representation, instance=instance)
        return representation


class OptionCategoryUpdateSerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)

    class Meta:
        model = OptionCategory
        fields = "__all__"
        read_only_fields = ("slug", "number", "studio",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(OptionCategoryUpdateSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        representation = get_file_representations(representation=representation, instance=instance)
        return representation


class OptionShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionCategory
        fields = ["id", "number", "title", "slug"]
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(OptionShortInfoSerializer, self).to_representation(instance)
        representation['option_category_details'] = OptionCategoryShortInfoSerializer(instance.option_category).data
        return representation

class OptionSerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)

    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(OptionSerializer, self).to_representation(instance)
        representation['option_category_details'] = OptionCategoryShortInfoSerializer(instance.option_category).data
        return representation


class OptionUpdateSerializer(DynamicMixinModelSerializer):
    icon = HybridImageField(required=False)

    class Meta:
        model = Option
        fields = "__all__"
        read_only_fields = ("slug", "option_category", "number",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(OptionUpdateSerializer, self).to_representation(instance)
        representation['option_category_details'] = OptionCategoryShortInfoSerializer(instance.option_category).data
        return representation
    
        
class PlanSerializer(DynamicMixinModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)

    class Meta:
        model = Plan
        fields = [
            "id", "title", "slug", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(PlanSerializer, self).to_representation(instance)
        representation['space_details'] = [SpaceShortInfoSerializer(spaceData).data for spaceData in instance.space.all()]
        representation['option_details'] = [OptionShortInfoSerializer(optionData).data for optionData in instance.option.all()]
        return representation

class PlanUpdateSerializer(DynamicMixinModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)

    class Meta:
        model = Plan
        fields = [
            "id", "title", "slug", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(PlanUpdateSerializer, self).to_representation(instance)
        representation['space_details'] = [SpaceShortInfoSerializer(spaceData).data for spaceData in instance.space.all()]
        representation['option_details'] = [OptionShortInfoSerializer(optionData).data for optionData in instance.option.all()]
        return representation
