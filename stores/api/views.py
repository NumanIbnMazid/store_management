from .serializers import (
    StoreSerializer, StoreUpdateSerializer, CustomBusinessDaySerializer, CustomBusinessDayUpdateSerializer, StoreModeratorSerializer,
    StoreModeratorUpdateSerializer
)
from stores.models import Store, CustomBusinessDay, StoreModerator
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from utils.studio_getter_helper import (
    get_studio_id_from_studio, get_studio_id_from_store
)
from dateutil import parser

class StoreManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Store.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_studio(selfObject=self, slug=self.kwargs.get("studio_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = StoreUpdateSerializer
        else:
            self.serializer_class = StoreSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]


    def list(self, request, *args, **kwargs):
        try:
            studio_slug = kwargs.get("studio_slug")
            qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='success')
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="list", error_code=400)
    
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(StoreManagerViewSet, self)._clean_data(data)


class CustomBusinessDayManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = CustomBusinessDay.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_store(selfObject=self, slug=self.kwargs.get("store_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = CustomBusinessDayUpdateSerializer
        else:
            self.serializer_class = CustomBusinessDaySerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def update(self, request, **kwargs):
        
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                date = request.data.get("date", None)
                status = request.data.get('status', None)
                
                store_custom_business_day_qs = CustomBusinessDay.objects.filter(
                    date=date, store=self.get_object().store
                ).exclude(slug__iexact=kwargs["slug"])
                if store_custom_business_day_qs.exists():
                    error_message = f"Date `{date}` already exists!"
                    return ResponseWrapper(error_code=400, error_msg=error_message, msg="Failed to update!", status=400)
                
                store_default_closed_day_of_weeks = self.get_object().store.default_closed_day_of_weeks
                
                date_obj = parser.parse(date)
                
                if date_obj.strftime("%A") in store_default_closed_day_of_weeks and int(status) == 0:
                    return ResponseWrapper(error_code=400, error_msg="Failed", msg=f"Date `{date} - {date_obj.strftime('%A')}` is alerady exists in Store Default Closed Day of Weeks!", status=400)
                if date_obj.strftime("%A") not in store_default_closed_day_of_weeks and int(status) == 1:
                    return ResponseWrapper(error_code=400, error_msg="Failed", msg=f"Date `{date} - {date_obj.strftime('%A')}` is alerady a Business Day!", status=400)
                
                qs = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)
                serializer = self.serializer_class(instance=qs)
                return ResponseWrapper(data=serializer.data)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="update", error_code=400)


        
"""
----------------------- * StoreModerator * -----------------------
"""


class StoreModeratorManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    queryset = StoreModerator.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_store(selfObject=self, slug=self.kwargs.get("store_slug"))

    def get_serializer_class(self):
        if self.action in ["create_admin"]:
            self.serializer_class = StoreModeratorSerializer
        if self.action in ["update"]:
            self.serializer_class = StoreModeratorUpdateSerializer
        else:
            self.serializer_class = StoreModeratorSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ["create_admin", "destroy_admin"]:
            permission_classes = [custom_permissions.IsSuperUser]
        elif self.action in ["create_staff", "destroy_staff","list"]:
            permission_classes = [custom_permissions.IsStudioAdmin]
        else:
            permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]

    # def create_admin(self, request, *args, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     serializer = serializer_class(data=request.data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         user_instance = serializer.save_base_user(request)
    #         # update is_studio_admin and is_store_staff in user model
    #         user_instance.is_studio_admin = True
    #         user_instance.is_store_staff = True
    #         user_instance.save()
    #         # save studio moderator
    #         moderator_instance = serializer.save(user=user_instance)
    #         # update is_admin and is_staff = True to make user studio admin
    #         moderator_instance.is_admin = True
    #         moderator_instance.is_staff = True
    #         # save moderator instacne
    #         moderator_instance.save()
    #         return ResponseWrapper(data=serializer.data, status=200)
    #     return ResponseWrapper(error_code=400, error_msg=serializer.errors)
    
    # def destroy_admin(self, request, **kwargs):
    #     qs = self.queryset.filter(**kwargs).first()
    #     if qs:
    #         qs.delete()
    #         return ResponseWrapper(status=200, msg='deleted')
    #     return ResponseWrapper(error_msg="failed to delete", error_code=400)

    def create_staff(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                user_instance = serializer.save_base_user(request)
                # update is_store_staff in user model
                user_instance.is_store_staff = True
                user_instance.save()
                # save studio moderator
                moderator_instance = serializer.save(user=user_instance)
                # update is_staff = True to make user studio staff
                moderator_instance.is_staff = True
                # save moderator instacne
                moderator_instance.save()
                return ResponseWrapper(data=serializer.data, status=200, msg="create")
            return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg="create")
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="create", error_code=400)

    def destroy_staff(self, request, **kwargs):
        try:
            qs = self.queryset.filter(**kwargs).first()
            if qs:
                qs.delete()
                return ResponseWrapper(status=200, msg='delete')
            return ResponseWrapper(error_msg="Failed to delete", error_code=400)
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="delete", error_code=400)

    def update(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True, context={"initialObject": self.get_object()})
            if serializer.is_valid():
                qs = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)
                serializer = self.serializer_class(instance=qs)
                qs.user.name = request.data.get('user', {}).get("name", None)
                qs.user.save()
                return ResponseWrapper(data=serializer.data, status=200, msg="update")
            return ResponseWrapper(error_msg=serializer.errors, error_code=400, msg="update")
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="update", error_code=400)
    
    def list(self, request, *args, **kwargs):
        try:
            store_slug = kwargs.get("store_slug")
            qs = self.get_queryset().filter(store__slug__iexact=store_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list', status=200)
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="list", error_code=400)
