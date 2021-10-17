from rest_framework import serializers
from studios.models import Studio, VatTax, Currency
from django.contrib.auth import get_user_model
from django.db import transaction
from users.api.serializers import (RegisterSerializer)
from utils.helpers import ResponseWrapper
from utils.mixins import DynamicMixinModelSerializer


"""
----------------------- * User Serializer * -----------------------
"""
class UserSerializer(DynamicMixinModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "username", "name", "slug", "is_studio_admin", "updated_at", "is_active", "last_login", "date_joined"
        ]
        
        
"""
----------------------- * Studio * -----------------------
"""


class StudioSerializer(DynamicMixinModelSerializer):
    user = RegisterSerializer(read_only=True)
    slug = serializers.ReadOnlyField()
    
    class Meta:
        model = Studio
        fields = '__all__'
        read_only_fields = ('slug',)
        
    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StudioSerializer, self).to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

    @transaction.atomic
    def save_base_user(self, request):
        try:
            user_data = request.data.get("user", {})
            register_serializer = RegisterSerializer(data=user_data)
            if register_serializer.is_valid(raise_exception=True):
                instance = register_serializer.save(request)
                # alter is_studio_admin = True
                instance.is_studio_admin = True
                # alter is_store_staff = True
                instance.is_store_staff = True
                instance.save()
                return instance
            if register_serializer.errors:
                raise serializers.ValidationError(register_serializer.errors)
            return ResponseWrapper(data=register_serializer.data, status=200)
        except Exception as E:
            raise serializers.ValidationError(E)


class StudioUpdateSerializer(DynamicMixinModelSerializer):
    
    class Meta:
        model = Studio
        fields = '__all__'
        read_only_fields = ("slug", "user")
        
    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StudioUpdateSerializer, self).to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

    

class VatTaxSerializer(DynamicMixinModelSerializer):
    class Meta:
        model = VatTax
        fields = "__all__"
        read_only_fields = ("slug",)
        
class VatTaxUpdateSerializer(DynamicMixinModelSerializer):
    class Meta:
        model = VatTax
        fields = "__all__"
        read_only_fields = ("slug","studio",)

class StudioVatTaxSerializer(serializers.Serializer):
    studio = serializers.IntegerField()


class StudioNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ["name"]
class CurrencySerializer(DynamicMixinModelSerializer):

    class Meta:
        model = Currency
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(CurrencySerializer, self).to_representation(instance)
        representation['studio'] = StudioNameSerializer(instance.studio).data
        return representation
        
class CurrencyUpdateSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = Currency
        fields = "__all__"
        read_only_fields = ("slug","studio")
