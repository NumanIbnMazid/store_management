from utils.mixins import DynamicMixinModelSerializer
from rest_framework import serializers
from spaces.models import Space
from drf_extra_fields.fields import HybridImageField
from stores.api.serializers import StoreShortInfoSerializer
from utils.helpers import get_file_representations


class SpaceShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ["id", "name", "slug"]

    def to_representation(self, instance):
        """ Modify representation of data """
        representation = super(SpaceShortInfoSerializer, self).to_representation(instance)
        representation['store_details'] = StoreShortInfoSerializer(instance.store).data
        return representation

class SpaceSerializer(DynamicMixinModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    image_4 = HybridImageField(required=False)
    image_5 = HybridImageField(required=False)

    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data integrating `studio` """
        representation = super(SpaceSerializer, self).to_representation(instance)
        representation['store_details'] = StoreShortInfoSerializer(instance.store).data
        representation = get_file_representations(representation=representation, instance=instance)
        return representation
    
class SpaceUpdateSerializer(DynamicMixinModelSerializer):
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    image_4 = HybridImageField(required=False)
    image_5 = HybridImageField(required=False)
    
    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("slug", "store")
        
    def to_representation(self, instance):
        """ Modify representation of data integrating `studio` """
        representation = super(SpaceUpdateSerializer, self).to_representation(instance)
        representation['store_details'] = StoreShortInfoSerializer(instance.store).data
        representation = get_file_representations(representation=representation, instance=instance)
        return representation
