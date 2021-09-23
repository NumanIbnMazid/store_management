from rest_framework import serializers
from spaces.models import Space

class SpaceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("slug",)

class SpaceUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("slug", "store")