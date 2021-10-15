from rest_framework import serializers
from django.db import transaction
from users.api.serializers import (
    RegisterSerializer
)
from utils.helpers import ResponseWrapper
from customers.models import Customer
from django.contrib.auth import get_user_model


class UserCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "username", "name", "slug", "is_customer", "updated_at", "is_active", "last_login", "date_joined"
        ]


class UserCustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["name"]


class CustomerSerializer(serializers.ModelSerializer):
    user = RegisterSerializer(read_only=True)
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = "__all__"

    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(CustomerSerializer, self).to_representation(instance)
        representation['user'] = UserCustomerSerializer(instance.user).data
        return representation

    @transaction.atomic
    def save_base_user(self, request):
        user_data = request.data.get("user", {})
        register_serializer = RegisterSerializer(data=user_data)
        if register_serializer.is_valid():
            instance = register_serializer.save(request)
            # alter is_customer = True
            instance.is_customer = True
            instance.save()
            return instance
        if register_serializer.errors:
            raise serializers.ValidationError(register_serializer.errors)
        return ResponseWrapper(data=register_serializer.data, status=200)

class CustomerUpdateSerializer(serializers.ModelSerializer):
    user = UserCustomerUpdateSerializer(read_only=True)
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = "__all__"

    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(CustomerUpdateSerializer, self).to_representation(instance)
        representation['user'] = UserCustomerSerializer(instance.user).data
        return representation


class CustomerSearchSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
     