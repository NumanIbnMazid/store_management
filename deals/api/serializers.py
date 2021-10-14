from rest_framework import serializers
from deals.models import Coupon, PointSetting

class CouponSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ("slug",)
        
class CouponUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ("slug","studio",)


class PointSettingSerializer(serializers.ModelSerializer):
      
    class Meta:
        model = PointSetting
        fields = "__all__"
        read_only_fields = ("slug",)
        
class PointSettingUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PointSetting
        fields = "__all__"
        read_only_fields = ("slug","studio",)