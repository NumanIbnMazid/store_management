from deals.models import Coupon, PointSetting, PeriodicalDiscount, EarlyBirdDiscount
from utils.mixins import DynamicMixinModelSerializer
from studios.api.serializers import StudioShortInfoSerializer
from rest_framework import serializers
from dateutil import parser


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
    
    def validate(self, data):
        
        # validate initials
        self.validate_initials(attrs=data)
        
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        
        if (start_date and not end_date) or (end_date and not start_date):
            raise serializers.ValidationError("You must provide both start date and end date!")
        
        if start_date and end_date:
            # check if start date and end date is in valid format
            start_date_obj = parser.parse(str(start_date))
            end_date_obj = parser.parse(str(end_date))
            
            if not end_date_obj > start_date_obj:
                raise serializers.ValidationError("End Date must be greater than Start Date!")
        return data
        

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
    
    def validate(self, data):
        
        # validate initials
        self.validate_initials(attrs=data)
        
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        
        if (start_date and not end_date) or (end_date and not start_date):
            raise serializers.ValidationError("You must provide both start date and end date!")
        
        if start_date and end_date:
            # check if start date and end date is in valid format
            start_date_obj = parser.parse(str(start_date))
            end_date_obj = parser.parse(str(end_date))
            
            if not end_date_obj > start_date_obj:
                raise serializers.ValidationError("End Date must be greater than Start Date!")
        return data
        
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
