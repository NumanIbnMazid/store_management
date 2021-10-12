from rest_framework import serializers
from stores.models import Store, CustomClosedDay
from drf_extra_fields.fields import HybridImageField
from middlewares.request_middleware import RequestMiddleware

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
        
    def validate(self, data):
        # validate if custom closed day exists for the provided store
        date = data['date']
        store = data['store']
        custom_closed_day_qs = CustomClosedDay.objects.filter(store=store, date=date)
        if custom_closed_day_qs:
            raise serializers.ValidationError(f"Date `{date}` is alerady exists in Custom Closed Day!")
        return data


class CustomClosedDayUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomClosedDay
        fields = "__all__"
        read_only_fields = ("slug", "store",)
        
    # def validate_date(self, value):
    #     # validate if custom closed day exists for the provided store
    #     print(value, "jhjhjhjhjhjhjhj")
    #     print(self.context, "ccccccccccccccccc")
    #     request = self.context['request']
    #     print(request, "ffffffffff")
    #     return value
        
    def validate(self, data):
        # validate if custom closed day exists for the provided store
        print(data, "ccccccccccccccccc")
        # request = self.context['request']
        # date = data['date']
        # slug = request.query_params['slug']
        # print(request, slug, "asdsadasdsad")
        # custom_closed_day_qs = CustomClosedDay.objects.filter(date=date)
        # if custom_closed_day_qs:
        #     raise serializers.ValidationError(
        #         f"Date `{date}` is alerady exists in Custom Closed Day!")
        return data
