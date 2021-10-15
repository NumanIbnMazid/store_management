from rest_framework import serializers
from stores.models import Store, CustomBusinessDay
from drf_extra_fields.fields import HybridImageField
from utils.mixins import DynamicMixinModelSerializer

class StoreSerializer(DynamicMixinModelSerializer):
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

class StoreUpdateSerializer(DynamicMixinModelSerializer):
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

class CustomBusinessDaySerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = CustomBusinessDay
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def validate(self, data):
        date = data.get("date", None)
        store = data.get('store', None)
        status = data.get('status', None)
        
        store_qs = Store.objects.filter(id=int(store.id))
        if store_qs:
            store_default_closed_day_of_weeks = store_qs.first().default_closed_day_of_weeks
            if date.strftime("%A") in store_default_closed_day_of_weeks and int(status) == 0:
                raise serializers.ValidationError(f"Date `{date} - {date.strftime('%A')}` is alerady exists in Store Default Closed Day of Weeks!")
            if date.strftime("%A") not in store_default_closed_day_of_weeks and int(status) == 1:
                raise serializers.ValidationError(f"Date `{date} - {date.strftime('%A')}` is alerady a Business Day!")
        else:
            raise serializers.ValidationError("Store not found!")
        
        custom_business_day_qs = CustomBusinessDay.objects.filter(store__id=store.id, date=date)
        if custom_business_day_qs:
            raise serializers.ValidationError(f"Date `{date}` is alerady exists in Custom Closed Day!")
        return data


class CustomBusinessDayUpdateSerializer(DynamicMixinModelSerializer):
    class Meta:
        model = CustomBusinessDay
        fields = "__all__"
        read_only_fields = ("slug", "store",)
