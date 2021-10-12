from rest_framework import serializers
from stores.models import Store, CustomClosedDay
from drf_extra_fields.fields import HybridImageField

class StoreSerializer(serializers.ModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def validate(self, data):
        default_closed_days = data['default_closed_days']
        valid_days = [
            "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        ]
        if not type(default_closed_days) == list:
            raise serializers.ValidationError("Invalid data type received! Expected List/Array.")
        
        for data in default_closed_days:
            if data.title() not in valid_days:
                raise serializers.ValidationError(f"Invalid data received `{data}`! Available `default_closed_days` are `{valid_days}`")
        return data

class StoreUpdateSerializer(serializers.ModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ("slug", "studio",)
        
    def validate(self, data):
        default_closed_days = data['default_closed_days']
        valid_days = [
            "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        ]
        if not type(default_closed_days) == list:
            raise serializers.ValidationError("Invalid data type received! Expected List/Array.")
        
        for data in default_closed_days:
            if data.title() not in valid_days:
                raise serializers.ValidationError(f"Invalid data received `{data}`! Available `default_closed_days` are `{valid_days}`")
        return data

class CustomClosedDaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomClosedDay
        fields = "__all__"
        read_only_fields = ("slug",)


class CustomClosedDayUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomClosedDay
        fields = "__all__"
        read_only_fields = ("slug", "store",)
