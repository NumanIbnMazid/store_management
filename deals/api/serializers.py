from rest_framework import serializers
from deals.models import Coupon
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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
        
    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = Coupon.objects.get(**self.initial_data)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return super().is_valid(raise_exception)
            else:
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            return super().is_valid(raise_exception)
