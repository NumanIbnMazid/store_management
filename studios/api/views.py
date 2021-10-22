from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper, get_exception_error_msg
from .serializers import (
    StudioSerializer,
    StudioUpdateSerializer,
    StudioShortInfoSerializer
    )
from studios.models import Studio
from allauth.utils import email_address_exists



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
        elif self.action in ["update", "put"]:
            self.serializer_class = StudioUpdateSerializer
        elif self.action in ["list_with_short_info"]:
            self.serializer_class = StudioShortInfoSerializer
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
            
            # validate user data
            errors = {}
            user_data = request.data.get("user", {})
            email = user_data.get("email", None)
            password1 = user_data.get("password1", None)
            password2 = user_data.get("password2", None)
            if email == None or email == "":
                errors["email"] = ["Email field is required!"]
            if password1 == None or password1 == "":
                errors["password1"] = ["Password field is required!"]
            if password1 != password2:
                errors["password1"] = ["Password didn't match!"]
            if email and email_address_exists(email):
                errors["email"] = ["A user is already registered with this e-mail address."]
                
                
            if serializer.is_valid(raise_exception=False):
                user_instance = serializer.save_base_user(request)
                studio_instance = serializer.save(user=user_instance)
                return ResponseWrapper(data=serializer.data, status=200)
            else:
                errors.update(serializer.errors)
            
            if len(errors):
                return ResponseWrapper(error_code=400, error_msg=errors, msg="Failed to create user!")
            
            return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg="create")
        
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="create")


    def update(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True, context={
                "initialObject": self.get_object(), "requestObject": request
            })
            if serializer.is_valid():
                qs = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)
                serializer = self.serializer_class(instance=qs)
                return ResponseWrapper(data=serializer.data, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400, msg="update")
        
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="update")
        
    def list_with_short_info(self, request):
        try:
            qs = self.get_queryset()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg="list", status=200)
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="list")
