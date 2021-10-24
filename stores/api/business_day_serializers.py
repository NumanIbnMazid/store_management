from rest_framework import serializers
from stores.models import Store
from studios.models import Studio
import datetime
from dateutil import parser


class StudioShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ["id", "name", "slug"]


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
            raise serializers.ValidationError(f"`year` field is required! Please input year as `YYYY`")
        # check if year is in valid format
        year = datetime.datetime.today().year
        year_list = list(range(year, year + 50))
        if not int(year) in year_list:
            raise serializers.ValidationError(f"Invalid data format year: {year}! Please input year as `YYYY`. Example: 2023")
        return data


class RangeBusinessDaysCheckerSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    
    def validate(self, data):
        start_date = str(data.get("start_date", None))
        end_date = str(data.get("end_date", None))
        if start_date == None or start_date == "" or end_date == None or end_date == "":
            raise serializers.ValidationError(
                f"`start_date` and `end_date` field is required! Please input date as `YYYY-MM-DD`"
            )
            
        # check if start date and end date is in valid format
        start_date_obj = parser.parse(start_date)
        end_date_obj = parser.parse(end_date)
        
        if not end_date_obj > start_date_obj:
            raise serializers.ValidationError(f"End Date must be greater than Start Date!")
        return data
