from rest_framework import serializers
from stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ("slug",)

class StoreUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ("slug", "studio",)