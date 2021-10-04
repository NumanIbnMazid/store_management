from rest_framework import serializers
from spaces.models import Space
from utils.base64_image import Base64ImageField

class SpaceSerializer(serializers.ModelSerializer):
    image_1 = Base64ImageField(max_length=None, use_url=True)
    image_2 = Base64ImageField(max_length=None, use_url=True)
    image_3 = Base64ImageField(max_length=None, use_url=True)
    image_4 = Base64ImageField(max_length=None, use_url=True)
    image_5 = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("slug",)

class SpaceUpdateSerializer(serializers.ModelSerializer):
    image_1 = Base64ImageField(max_length=None, use_url=True)
    image_2 = Base64ImageField(max_length=None, use_url=True)
    image_3 = Base64ImageField(max_length=None, use_url=True)
    image_4 = Base64ImageField(max_length=None, use_url=True)
    image_5 = Base64ImageField(max_length=None, use_url=True)
    
    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("slug", "store")