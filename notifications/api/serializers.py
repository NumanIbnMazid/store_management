from rest_framework import serializers
from notifications.models import Notification
from drf_extra_fields.fields import HybridImageField

class NotificationSerializer(serializers.ModelSerializer):
    file = HybridImageField(required=False)
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("slug",)

class NotificationUpdateSerializer(serializers.ModelSerializer):
    file = HybridImageField(required=False)
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("slug", "studio",)


class NotificationPublishedSerializer(serializers.Serializer):
    studio = serializers.IntegerField()
