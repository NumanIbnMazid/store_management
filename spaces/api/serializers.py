from rest_framework import serializers
from spaces.models import Space
from drf_extra_fields.fields import HybridImageField
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


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
        
    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = Space.objects.get(**self.initial_data)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return super().is_valid(raise_exception)
            else:
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            return super().is_valid(raise_exception)
