from rest_framework import serializers
from stores.models import StoreBusinessHour

class StoreBusinessHourSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StoreBusinessHour
        fields = "__all__"
        read_only_fields = ("slug",)

class StoreBusinessHourUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreBusinessHour
        fields = "__all__"
        read_only_fields = ("slug", "store",)
