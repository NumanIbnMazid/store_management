from rest_framework import serializers
from stores.models import Store
from utils.base64_image import Base64ImageField

class StoreSerializer(serializers.ModelSerializer):
    image_1 = Base64ImageField(max_length=None, use_url=True)
    image_2 = Base64ImageField(max_length=None, use_url=True)
    image_3 = Base64ImageField(max_length=None, use_url=True)
   
    
    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ("slug",)

class StoreUpdateSerializer(serializers.ModelSerializer):
    image_1 = Base64ImageField(max_length=None, use_url=True)
    image_2 = Base64ImageField(max_length=None, use_url=True)
    image_3 = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ("slug", "studio",)