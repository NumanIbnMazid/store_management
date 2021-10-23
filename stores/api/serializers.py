from rest_framework import serializers
from stores.models import Store, CustomBusinessDay, StoreModerator
from studios.models import Studio
from drf_extra_fields.fields import HybridImageField
from utils.mixins import DynamicMixinModelSerializer
from django.contrib.auth import get_user_model
from users.api.serializers import (RegisterSerializer)
from django.db import transaction
from utils.helpers import ResponseWrapper, get_file_representations
from stores.models import StoreBusinessHour
from utils.mixins import DynamicMixinModelSerializer

"""
----------------------- * Store * -----------------------
"""

class StudioShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ["id", "name", "slug"]

class StoreShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "slug"]

class StoreSerializer(DynamicMixinModelSerializer):
    studio_details = serializers.CharField(read_only=True)
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    studio = serializers.PrimaryKeyRelatedField(queryset=Studio.objects.all())
    
    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ("slug",)
        extra_kwargs = {'default_closed_day_of_weeks': {'required': True}}
        
    def validate(self, data):
        
        # validate initials
        self.validate_initials(attrs=data)
        
        default_closed_day_of_weeks = data.get("default_closed_day_of_weeks", None)
        if default_closed_day_of_weeks:
            valid_day_of_weeks = [
                "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
            ]
            if not type(default_closed_day_of_weeks) == list:
                raise serializers.ValidationError("Invalid data type received! Expected List/Array.")
            for day_of_week in default_closed_day_of_weeks:
                if day_of_week.title() not in valid_day_of_weeks:
                    raise serializers.ValidationError(f"Invalid data received `{day_of_week}`! Available `default_closed_day_of_weeks` are `{valid_day_of_weeks}`")
        return data
    
    def to_representation(self, instance):
        """ Modify representation of data integrating `studio` """
        representation = super(StoreSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        representation = get_file_representations(representation=representation, instance=instance)
        return representation

class StoreUpdateSerializer(DynamicMixinModelSerializer):
    studio_details = serializers.CharField(read_only=True)
    image_1 = HybridImageField(required=False)
    image_2 = HybridImageField(required=False)
    image_3 = HybridImageField(required=False)
    
    class Meta:
        model = Store
        fields = "__all__"
        read_only_fields = ("slug", "studio",)
        extra_kwargs = {'default_closed_day_of_weeks': {'required': True}}
        
    def validate(self, data):
        
        # validate initials
        self.validate_initials(attrs=data)
        
        default_closed_day_of_weeks = data.get("default_closed_day_of_weeks", None)
        if default_closed_day_of_weeks:
            valid_day_of_weeks = [
                'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'
            ]
            if not type(default_closed_day_of_weeks) == list:
                raise serializers.ValidationError("Invalid data type received! Expected List/Array.")
            
            for day_of_week in default_closed_day_of_weeks:
                if day_of_week.title() not in valid_day_of_weeks:
                    raise serializers.ValidationError(f"Invalid data received `{day_of_week}`! Available `default_closed_day_of_weeks` are `{valid_day_of_weeks}`")
        return data
    
    def to_representation(self, instance):
        """ Modify representation of data integrating `studio` """
        representation = super(StoreUpdateSerializer, self).to_representation(instance)
        representation['studio_details'] = StudioShortInfoSerializer(instance.studio).data
        representation = get_file_representations(representation=representation, instance=instance)
        return representation
    

"""
----------------------- * CustomBusinessDay * -----------------------
"""

class CustomBusinessDaySerializer(DynamicMixinModelSerializer):
    store_details = serializers.CharField(read_only=True)
    
    class Meta:
        model = CustomBusinessDay
        fields = "__all__"
        read_only_fields = ("slug",)
        
    def validate(self, data):
        
        # validate initials
        self.validate_initials(attrs=data)
        
        date = data.get("date", None)
        store = data.get('store', None)
        status = data.get('status', None)
        
        store_qs = Store.objects.filter(id=int(store.id))
        if store_qs:
            store_default_closed_day_of_weeks = store_qs.first().default_closed_day_of_weeks
            if date.strftime("%A") in store_default_closed_day_of_weeks and int(status) == 0:
                raise serializers.ValidationError(f"Date `{date} - {date.strftime('%A')}` is alerady exists in Store Default Closed Day of Weeks!")
            if date.strftime("%A") not in store_default_closed_day_of_weeks and int(status) == 1:
                raise serializers.ValidationError(f"Date `{date} - {date.strftime('%A')}` is alerady a Business Day!")
        else:
            raise serializers.ValidationError("Store not found!")
        
        custom_business_day_qs = CustomBusinessDay.objects.filter(store__id=store.id, date=date)
        if custom_business_day_qs:
            raise serializers.ValidationError(f"Date `{date}` is alerady exists in Custom Closed Day!")
        return data
    
    def to_representation(self, instance):
        """ Modify representation of data integrating `studio` """
        representation = super(CustomBusinessDaySerializer, self).to_representation(instance)
        representation['store_details'] = StoreShortInfoSerializer(instance.store).data
        return representation


class CustomBusinessDayUpdateSerializer(DynamicMixinModelSerializer):
    store_details = serializers.CharField(read_only=True)
    class Meta:
        model = CustomBusinessDay
        fields = "__all__"
        read_only_fields = ("slug", "store",)
        
    def validate(self, data):
        
        # validate initials
        self.validate_initials(attrs=data)
        
        date = data.get("date", None)
        store = data.get('store', None)
        status = data.get('status', None)
        
        store_qs = Store.objects.filter(id=int(store.id))
        if store_qs:
            store_default_closed_day_of_weeks = store_qs.first().default_closed_day_of_weeks
            if date.strftime("%A") in store_default_closed_day_of_weeks and int(status) == 0:
                raise serializers.ValidationError(f"Date `{date} - {date.strftime('%A')}` is alerady exists in Store Default Closed Day of Weeks!")
            if date.strftime("%A") not in store_default_closed_day_of_weeks and int(status) == 1:
                raise serializers.ValidationError(f"Date `{date} - {date.strftime('%A')}` is alerady a Business Day!")
        else:
            raise serializers.ValidationError("Store not found!")
        
        custom_business_day_qs = CustomBusinessDay.objects.filter(store__id=store.id, date=date)
        if custom_business_day_qs:
            raise serializers.ValidationError(f"Date `{date}` is alerady exists in Custom Closed Day!")
        return data
        
    def to_representation(self, instance):
        """ Modify representation of data integrating `studio` """
        representation = super(CustomBusinessDayUpdateSerializer, self).to_representation(instance)
        representation['store_details'] = StoreShortInfoSerializer(instance.store).data
        return representation


"""
----------------------- * StoreModerator * -----------------------
"""

""" *** Studio Moderator *** """
class UserStoreModeratorSerializer(DynamicMixinModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id", "email", "username", "name", "slug", "is_store_staff", "updated_at", "is_active", "last_login", "date_joined"
        ]
        

class UserStoreModeratorUpdateSerializer(DynamicMixinModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["name"]


class StoreIDSerializer(DynamicMixinModelSerializer):
    class Meta:
        model = Store
        fields = ["id"]
        extra_kwargs = {'id': {'required': True}}


class StoreModeratorSerializer(DynamicMixinModelSerializer):
    user = RegisterSerializer(read_only=True)
    store_details = serializers.CharField(read_only=True)
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all(), many=True)

    class Meta:
        model = StoreModerator
        fields = "__all__"
        read_only_fields = ("is_staff", "slug",)


    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StoreModeratorSerializer, self).to_representation(instance)
        representation['user'] = UserStoreModeratorSerializer(instance.user).data
        representation['store_details'] = [StoreShortInfoSerializer(storeData).data for storeData in instance.store.all()]
        return representation


    @transaction.atomic
    def save_base_user(self, request):
        user_data = request.data.get("user", {})
        register_serializer = RegisterSerializer(data=user_data)
        if register_serializer.is_valid():
            instance = register_serializer.save(request)
            # alter is_store_staff = True
            instance.is_store_staff = True
            instance.save()
            return instance
        if register_serializer.errors:
            raise serializers.ValidationError(register_serializer.errors)
        return ResponseWrapper(data=register_serializer.data, status=200)
    

class StoreModeratorUpdateSerializer(DynamicMixinModelSerializer):
    user = UserStoreModeratorUpdateSerializer(read_only=True)
    store_details = serializers.CharField(read_only=True)
    
    class Meta:
        model = StoreModerator
        fields = ["user", "store", "contact", "address", "store_details"]

    def to_representation(self, instance):
        """ Modify representation of data integrating `user` OneToOne Field """
        representation = super(StoreModeratorUpdateSerializer, self).to_representation(instance)
        representation['user'] = UserStoreModeratorSerializer(instance.user).data
        representation['store_details'] = [StoreShortInfoSerializer(storeData).data for storeData in instance.user.store_moderator_user.store.all()]
        return representation


class StoreBusinessHourSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreBusinessHour
        fields = "__all__"
        read_only_fields = ("slug",)


class StoreBusinessHourUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreBusinessHour
        fields = "__all__"
        read_only_fields = ("slug", "store",)
