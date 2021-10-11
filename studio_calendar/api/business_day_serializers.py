from rest_framework import serializers
from studio_calendar.models import BusinessDay
from stores.models import Store

class BusinessDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDay
        fields = "__all__"
        read_only_fields = ("slug", )


class YearBusinessDaySerializer(serializers.Serializer):
    pass


class SingleBusinessDayCheckerSerializer(serializers.Serializer):
    date = serializers.DateField()
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
