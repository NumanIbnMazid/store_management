from deals.models import Coupon, PointSetting
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
