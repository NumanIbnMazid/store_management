from rest_framework import serializers
from studios.models import Studio, VatTax, Currency
from django.contrib.auth import get_user_model
from django.db import transaction
from users.api.serializers import (RegisterSerializer)
from utils.helpers import ResponseWrapper
from utils.mixins import DynamicMixinModelSerializer
from rest_framework.validators import ValidationError


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
        raise serializers.ValidationError(register_serializer.errors)
        
    def to_internal_value(self, data):
        """Flatten nested error dict."""
        try:
            return super().to_internal_value(data)
        except ValidationError as error:
            print("except block is calling from to_internal_value *******")
            if not isinstance(error.detail, dict) or not self._list_fields:
                raise error
            errors = {}
            for key, value in error.detail.items():
                if key in self._list_fields and isinstance(value, dict):
                    # flatten nested dict out into parent dict
                    for list_key, list_value in value.items():
                        errors[f"{key}/{list_key}"] = list_value
                else:
                    errors[key] = value
            raise ValidationError(errors)


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
    

class StudioShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ["name", "slug"]

    

class VatTaxSerializer(DynamicMixinModelSerializer):
    studio_details = serializers.CharField(read_only=True)
    class Meta:
        model = VatTax
        fields = "__all__"
        read_only_fields = ("slug",)
    
    def to_representation(self, instance):
        """ Modify representation of data integrating `studio` """
        representation = super(VatTaxSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation
        
class VatTaxUpdateSerializer(DynamicMixinModelSerializer):
    class Meta:
        model = VatTax
        fields = "__all__"
        read_only_fields = ("slug","studio",)

class StudioVatTaxSerializer(serializers.Serializer):
    studio = serializers.IntegerField()

class CurrencySerializer(DynamicMixinModelSerializer):
    
    studio_details = serializers.CharField(read_only=True)

    class Meta:
        model = Currency
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def to_representation(self, instance):
        """ Modify representation of data integrating `studio` """
        representation = super(CurrencySerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        return representation
        
class CurrencyUpdateSerializer(DynamicMixinModelSerializer):

    class Meta:
        model = Currency
        fields = "__all__"
        read_only_fields = ("slug","studio")
