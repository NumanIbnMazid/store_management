from rest_framework import serializers
from stores.models import CustomClosedDay, Store


class BusinessDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())


class SingleBusinessDayCheckerSerializer(serializers.Serializer):
    date = serializers.DateField()
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    
    def validate(self, data):
        date = data.get("date", None)
        if date == None or date == "":
            raise serializers.ValidationError(f"`date` field is required! Please input date as `YYYY-MM-DD`")
        return data
