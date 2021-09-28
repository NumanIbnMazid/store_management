from rest_framework.serializers import Serializer
from rest_framework import serializers
from django.db import transaction
from users.api.serializers import (
    RegisterSerializer
)
from utils.helpers import ResponseWrapper
from staffs.models import Staff
from django.contrib.auth import get_user_model


class UserStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "username", "name", "slug", "is_staff", "is_superuser", "updated_at", "is_active", "last_login", "date_joined"
        ]


class UserStaffUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["name"]


class StaffSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(read_only=True)
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Staff
        fields = "__all__"

    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StaffSerializer, self).to_representation(instance)
        representation['user'] = UserStaffSerializer(instance.user).data
        return representation

    @transaction.atomic
    def save_base_user(self, request):
        user_data = request.data.get("user", {})
        register_serializer = RegisterSerializer(data=user_data)
        if register_serializer.is_valid():
            instance = register_serializer.save(request)
            # alter is_staff = True
            instance.is_staff = True
            instance.save()
            return instance
        if register_serializer.errors:
            raise serializers.ValidationError(register_serializer.errors)
        return ResponseWrapper(data=register_serializer.data, status=200)


class StaffUpdateSerializer(serializers.ModelSerializer):
    user = UserStaffUpdateSerializer(read_only=True)
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Staff
        fields = "__all__"

    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StaffUpdateSerializer, self).to_representation(instance)
        representation['user'] = UserStaffSerializer(instance.user).data
        return representation
