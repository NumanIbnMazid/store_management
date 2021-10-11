from rest_framework import serializers
from deals.models import Coupon

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