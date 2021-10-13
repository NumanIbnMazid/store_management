from rest_framework import serializers
from stores.models import CustomBusinessDay, Store
import datetime


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

class YearBusinessDaysCheckerSerializer(serializers.Serializer):
    year = serializers.CharField()
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    
    def validate(self, data):
        year = data.get("year", None)
        if year == None or year == "":
            raise serializers.ValidationError(f"`date` field is required! Please input date as `YYYY-MM-DD`")
        # check if year is in valid format
        year = datetime.datetime.today().year
        year_list = list(range(year, year + 50))
        if not int(year) in year_list:
            raise serializers.ValidationError(f"Invalid data format year: {year}! Please input year as `YYYY`. Example: 2023")
        return data
