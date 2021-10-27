from deals.models import Coupon, PointSetting, PeriodicalDiscount, EarlyBirdDiscount
from utils.mixins import DynamicMixinModelSerializer
from studios.api.serializers import StudioShortInfoSerializer


class CouponSerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(CouponSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation
        

class CouponUpdateSerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = Coupon
        fields = "__all__"
        read_only_fields = ("slug","studio",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(CouponUpdateSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation
        
class PointSettingSerializer(DynamicMixinModelSerializer):
      
    class Meta:
        model = PointSetting
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(PointSettingSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation
        

class PointSettingUpdateSerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = PointSetting
        fields = "__all__"
        read_only_fields = ("slug", "studio",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(PointSettingUpdateSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation


class PeriodicalDiscountSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = PeriodicalDiscount
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(PeriodicalDiscountSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation


class PeriodicalDiscountUpdateSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = PeriodicalDiscount
        fields = "__all__"
        read_only_fields = ("slug", "studio",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(PeriodicalDiscountUpdateSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation


class EarlyBirdDiscountSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = EarlyBirdDiscount
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(EarlyBirdDiscountSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation


class EarlyBirdDiscountUpdateSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = EarlyBirdDiscount
        fields = "__all__"
        read_only_fields = ("slug", "studio",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(EarlyBirdDiscountUpdateSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation
