from deals.models import Coupon, PointSetting, PeriodicalDiscount, EarlyBirdDiscount
from utils.mixins import DynamicMixinModelSerializer


class CouponSerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ("slug",)
        

class CouponUpdateSerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ("slug","studio",)
        
class PointSettingSerializer(DynamicMixinModelSerializer):
      
    class Meta:
        model = PointSetting
        fields = "__all__"
        read_only_fields = ("slug",)
        

class PointSettingUpdateSerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = PointSetting
        fields = "__all__"
        read_only_fields = ("slug", "studio",)


class PeriodicalDiscountSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = PeriodicalDiscount
        fields = "__all__"
        read_only_fields = ("slug",)


class PeriodicalDiscountUpdateSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = PeriodicalDiscount
        fields = "__all__"
        read_only_fields = ("slug", "studio",)


class EarlyBirdDiscountSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = EarlyBirdDiscount
        fields = "__all__"
        read_only_fields = ("slug",)


class EarlyBirdDiscountUpdateSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = EarlyBirdDiscount
        fields = "__all__"
        read_only_fields = ("slug", "studio",)
