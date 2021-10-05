from rest_framework import serializers
from spaces.models import Space
from drf_extra_fields.fields import HybridImageField

class SpaceSerializer(serializers.ModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    image_4 = HybridImageField(required=False)
    image_5 = HybridImageField(required=False)

    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("slug",)

class SpaceUpdateSerializer(serializers.ModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    image_4 = HybridImageField(required=False)
    image_5 = HybridImageField(required=False)
    
    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("slug", "store")
