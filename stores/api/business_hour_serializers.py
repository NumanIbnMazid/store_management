from rest_framework import serializers
from stores.models import StoreBusinessHour, Store
from stores.api.serializers import StoreShortInfoSerializer
from utils.mixins import DynamicMixinModelSerializer


class StoreBusinessHourSerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = StoreBusinessHour
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def validate(self, data):
        
        # validate initials
        self.validate_initials(attrs=data)
        
        day_of_weeks = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
        
        week_data = {}
        
        for key in data:
            if key.split("_")[0] in day_of_weeks:
                if key.split("_")[0] in week_data.keys():
                    pass
                else:
                    week_data[key.split("_")[0]] = {"opening": None, "closing": None}
                    
                if "opening" in key:
                    week_data[key.split("_")[0]]["opening"] = data.get(key)
                if "closing" in key:
                    week_data[key.split("_")[0]]["closing"] = data.get(key)
                    
        for key, value in week_data.items():
            if not value.get("closing") > value.get("opening"):
                raise serializers.ValidationError(
                    {key: f"{key.title()}: Closing time must be greater than opening time!"}
                )
       
        return data
        
    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(StoreBusinessHourSerializer, self).to_representation(instance)
        representation['store_details'] = StoreShortInfoSerializer(instance.store).data
        return representation

class StoreBusinessHourUpdateSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = StoreBusinessHour
        fields = "__all__"
        read_only_fields = ("slug", "store",)
        
    
    def validate(self, data):
        
        # validate initials
        self.validate_initials(attrs=data)
        
        day_of_weeks = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]
        
        week_data = {}
        
        for key in data:
            if key.split("_")[0] in day_of_weeks:
                if key.split("_")[0] in week_data.keys():
                    pass
                else:
                    week_data[key.split("_")[0]] = {"opening": None, "closing": None}
                    
                if "opening" in key:
                    week_data[key.split("_")[0]]["opening"] = data.get(key)
                if "closing" in key:
                    week_data[key.split("_")[0]]["closing"] = data.get(key)
                    
        for key, value in week_data.items():
            if not value.get("closing") > value.get("opening"):
                raise serializers.ValidationError(
                    {key: f"{key.title()}: Closing time must be greater than opening time!"}
                )
       
        return data


class BusinessHourFromWeekNameCheckerSerializer(serializers.Serializer):
    day_of_week = serializers.CharField(required=True)
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    
    def validate(self, data):
        day_of_week = data.get("day_of_week", None)
        if day_of_week:
            valid_day_of_weeks = [
                "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
            ]
            if day_of_week.title() not in valid_day_of_weeks:
                raise serializers.ValidationError(f"Invalid data received `{day_of_week}`! Available Week Names are `{valid_day_of_weeks}`")
        else:
            raise serializers.ValidationError("Day of Week Name is required!")
        return data

class BusinessHourFromDateCheckerSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
