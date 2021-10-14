from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from .serializers import StudioSerializer, StudioModeratorSerializer, StudioModeratorUpdateSerializer, StudioUpdateSerializer
from studios.models import Studio, StudioModerator
from utils.studio_getter_helper import (
    get_studio_id_from_studio
)


"""
----------------------- * Studio * -----------------------
"""
class StudioViewSet(LoggingMixin, CustomViewSet):
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Studio.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        try:
            return True, self.get_object().id
        except Exception as E:
            try:
                return True, self.request.user.studio_user.id
            except Exception as E:
                return False

    def get_serializer_class(self):
        if self.action in ["create"]:
            self.serializer_class = StudioSerializer
        elif self.action in ["update"]:
            self.serializer_class = StudioUpdateSerializer
        else:
            self.serializer_class = StudioSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ["create", "destroy", "list"]:
            permission_classes = [custom_permissions.IsSuperUser]
        else:
            permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                user_instance = serializer.save_base_user(request)
                studio_instance = serializer.save(user=user_instance)
                return ResponseWrapper(data=serializer.data, status=200)
            return ResponseWrapper(error_code=400, error_msg=serializer.errors)
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to create!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to create!", error_code=400)

    def update(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                qs = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)
                serializer = self.serializer_class(instance=qs)
                return ResponseWrapper(data=serializer.data, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to update!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to update!", error_code=400)
    


"""
----------------------- * StudioModerator * -----------------------
"""
class StudioModeratorManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    queryset = StudioModerator.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_studio(selfObject=self, slug=self.kwargs.get("studio_slug"))

    def get_serializer_class(self):
        if self.action in ["create_admin"]:
            self.serializer_class = StudioModeratorSerializer
        if self.action in ["update"]:
            self.serializer_class = StudioModeratorUpdateSerializer
        else:
            self.serializer_class = StudioModeratorSerializer
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
    #         # update is_studio_admin and is_studio_staff in user model
    #         user_instance.is_studio_admin = True
    #         user_instance.is_studio_staff = True
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
                # update is_studio_staff in user model
                user_instance.is_studio_staff = True
                user_instance.save()
                # save studio moderator
                moderator_instance = serializer.save(user=user_instance)
                # update is_staff = True to make user studio staff
                moderator_instance.is_staff = True
                # save moderator instacne
                moderator_instance.save()
                return ResponseWrapper(data=serializer.data, status=200)
            return ResponseWrapper(error_code=400, error_msg=serializer.errors)
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to create staff!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to create staff!", error_code=400)

    def destroy_staff(self, request, **kwargs):
        try:
            qs = self.queryset.filter(**kwargs).first()
            if qs:
                qs.delete()
                return ResponseWrapper(status=200, msg='deleted')
            return ResponseWrapper(error_msg="failed to delete", error_code=400)
        except Exception as E:
            return ResponseWrapper(error_msg=str(E), msg="Failed to delete!", error_code=400)

    def update(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                qs = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)
                serializer = self.serializer_class(instance=qs)
                qs.user.name = request.data.get('user', {}).get("name", None)
                qs.user.save()
                return ResponseWrapper(data=serializer.data, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to update!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to update!", error_code=400)
    
    def list(self, request, *args, **kwargs):
        try:
            studio_slug = kwargs.get("studio_slug")
            qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='success')
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to retrieve list!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to retrieve list!", error_code=400)
