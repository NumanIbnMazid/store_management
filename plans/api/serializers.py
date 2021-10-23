from plans.models import OptionCategory, Option, Plan
from drf_extra_fields.fields import HybridImageField
from utils.mixins import DynamicMixinModelSerializer
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
        read_only_fields = ("slug", "number", "studio",)


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
        read_only_fields = ("slug", "option_category", "number",)
        
class PlanSerializer(DynamicMixinModelSerializer):
    image_1 = Base64ImageField(max_length=None, use_url=True, required=False)
    image_2 = Base64ImageField(max_length=None, use_url=True, required=False)
    image_3 = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Plan
        fields = [
            "title", "slug", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)

class PlanUpdateSerializer(DynamicMixinModelSerializer):
    image_1 = Base64ImageField(max_length=None, use_url=True, required=False)
    image_2 = Base64ImageField(max_length=None, use_url=True, required=False)
    image_3 = Base64ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Plan
        fields = [
            "title", "slug", "space", "option", "hourly_price", "daily_price", "image_1", "image_1_reference", "image_1_comment", "image_2", "image_2_reference", "image_2_comment", "image_3", "image_3_reference", "image_3_comment", "is_active", "explanatory_comment", "details"
        ]
        read_only_fields = ("slug",)
