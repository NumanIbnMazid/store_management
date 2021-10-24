from rest_framework import serializers
from stores.models import StoreBusinessHour
from stores.api.serializers import StoreShortInfoSerializer


class StoreBusinessHourSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StoreBusinessHour
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(StoreBusinessHourSerializer, self).to_representation(instance)
        representation['store_details'] = StoreShortInfoSerializer(instance.store).data
        return representation

class StoreBusinessHourUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreBusinessHour
        fields = "__all__"
        read_only_fields = ("slug", "store",)


class BusinessHourFromWeekNameCheckerSerializer(serializers.Serializer):
    week_name = serializers.CharField()