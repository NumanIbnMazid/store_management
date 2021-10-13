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
        default_closed_day_of_weeks = data.get("default_closed_day_of_weeks")
        valid_day_of_weeks = [
            "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        ]
        if not type(default_closed_day_of_weeks) == list:
            raise serializers.ValidationError("Invalid data type received! Expected List/Array.")
        for day_of_week in default_closed_day_of_weeks:
            if day_of_week.title() not in valid_day_of_weeks:
                raise serializers.ValidationError(f"Invalid data received `{day_of_week}`! Available `default_closed_day_of_weeks` are `{valid_day_of_weeks}`")
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
        default_closed_day_of_weeks = data.get("default_closed_day_of_weeks")
        valid_day_of_weeks = [
            "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        ]
        if not type(default_closed_day_of_weeks) == list:
            raise serializers.ValidationError("Invalid data type received! Expected List/Array.")
        
        for day_of_week in default_closed_day_of_weeks:
            if day_of_week.title() not in valid_day_of_weeks:
                raise serializers.ValidationError(f"Invalid data received `{day_of_week}`! Available `default_closed_day_of_weeks` are `{valid_day_of_weeks}`")
        return data

class CustomClosedDaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomClosedDay
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def validate(self, data):
        # validate if custom closed day exists for the provided store
        date = data.get("date", None)
        store = data.gte('store', None)
        custom_closed_day_qs = CustomClosedDay.objects.filter(store=store, date=date)
        if custom_closed_day_qs:
            raise serializers.ValidationError(f"Date `{date}` is alerady exists in Custom Closed Day!")
        return data


class CustomClosedDayUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomClosedDay
        fields = "__all__"
        read_only_fields = ("slug", "store",)
