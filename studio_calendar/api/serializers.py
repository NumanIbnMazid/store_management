from django.db.models import fields
from rest_framework import serializers
from studio_calendar.models import StudioCalendar

class StudioCalendarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudioCalendar
        fields = "__all__"
        read_only_fields = ("slug", "country_code")


class StudioCalendarUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StudioCalendar
        fields = "__all__"
        read_only_fields = ("slug", "country_code", "studio")
        
class SingleHolidayCheckerSerializer(serializers.Serializer):
    date = serializers.DateField()
    studio = serializers.IntegerField()


class RangeHolidayCheckerSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    studio = serializers.IntegerField()


class YearHolidayCheckerSerializer(serializers.Serializer):
    year = serializers.CharField()
    studio = serializers.IntegerField()

class ListHolidayCheckerSerializer(serializers.Serializer):
    date_list = serializers.ListField()
    studio = serializers.IntegerField()
