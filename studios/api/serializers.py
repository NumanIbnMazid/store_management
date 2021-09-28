from rest_framework import fields, serializers
from studios.models import Studio, StudioModerator
from django.contrib.auth import get_user_model
from django.db import transaction
from users.api.serializers import (RegisterSerializer)
from utils.helpers import ResponseWrapper


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
            # alter is_customer = True
            instance.is_studio_admin = True
            instance.save()
            return instance
        if register_serializer.errors:
            raise serializers.ValidationError(register_serializer.errors)
        return ResponseWrapper(data=register_serializer.data, status=200)
        

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
