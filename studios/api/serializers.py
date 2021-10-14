from rest_framework import serializers
from studios.models import Studio, StudioModerator, VatTax, Currency
from django.contrib.auth import get_user_model
from django.db import transaction
from users.api.serializers import (RegisterSerializer)
from utils.helpers import ResponseWrapper
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


"""
----------------------- * User Serializer * -----------------------
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "username", "name", "slug", "is_customer", "updated_at", "is_active", "last_login", "date_joined"
        ]
"""
----------------------- * Studio * -----------------------
"""
class StudioSerializer(serializers.ModelSerializer):
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
        if register_serializer.is_valid():
            instance = register_serializer.save(request)
            # alter is_studio_admin = True
            instance.is_studio_admin = True
            # alter is_studio_staff = True
            instance.is_studio_staff = True
            instance.save()
            return instance
        if register_serializer.errors:
            raise serializers.ValidationError(register_serializer.errors)
        return ResponseWrapper(data=register_serializer.data, status=200)


class StudioUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Studio
        fields = '__all__'
        read_only_fields = ("slug", "user")
        
    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = Studio.objects.get(**self.initial_data)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return super().is_valid(raise_exception)
            else:
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            return super().is_valid(raise_exception)
        
    
    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StudioUpdateSerializer, self).to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

    
"""
----------------------- * StudioModerator * -----------------------
"""

""" *** Studio Moderator *** """
class UserStudioModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "username", "name", "slug", "updated_at", "is_active", "last_login", "date_joined"
        ]


class UserStudioModeratorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["name"]


class StudioModeratorSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(read_only=True)

    class Meta:
        model = StudioModerator
        fields = "__all__"
        read_only_fields = ("is_staff", "slug",)

    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StudioModeratorSerializer, self).to_representation(instance)
        representation['user'] = UserStudioModeratorSerializer(instance.user).data
        return representation

    @transaction.atomic
    def save_base_user(self, request):
        user_data = request.data.get("user", {})
        register_serializer = RegisterSerializer(data=user_data)
        if register_serializer.is_valid():
            instance = register_serializer.save(request)
            # alter is_studio_staff = True
            instance.is_studio_staff = True
            instance.save()
            return instance
        if register_serializer.errors:
            raise serializers.ValidationError(register_serializer.errors)
        return ResponseWrapper(data=register_serializer.data, status=200)


class StudioModeratorUpdateSerializer(serializers.ModelSerializer):
    user = UserStudioModeratorUpdateSerializer(read_only=True)
    
    class Meta:
        model = StudioModerator
        fields = ["user", "contact", "address"]

    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StudioModeratorUpdateSerializer, self).to_representation(instance)
        representation['user'] = UserStudioModeratorSerializer(instance.user).data
        return representation

class VatTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatTax
        fields = "__all__"
        read_only_fields = ("slug",)
        
class VatTaxUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VatTax
        fields = "__all__"
        read_only_fields = ("slug","studio",)

class StudioVatTaxSerializer(serializers.Serializer):
    studio = serializers.IntegerField()


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = "__all__"
        read_only_fields = ("slug",)
        
class CurrencyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = "__all__"
        read_only_fields = ("slug","studio")
