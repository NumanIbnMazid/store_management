from rest_auth.views import LoginView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import serializers
from django.contrib.auth import get_user_model
import json
from rest_framework_tracking.mixins import LoggingMixin
from utils.custom_viewset import CustomViewSet
from .serializers import UserSerializer, UserUpdateSerializer
from utils import permissions as custom_permissions
from utils.helpers import ResponseWrapper


class CustomAPILoginView(LoginView):
    def get_response(self):
        """[CustomAPILoginView: Integrates JWT Token and User Details with LoginView]

        Returns:
            [object]: [JWT_TOKEN{}, USER{}, KEY]
        """
        # get original response from LoginView
        original_response = super().get_response()
        
        # remove key from original response and store in a variable to organize response order
        key = original_response.data.pop("key")
        
        # get logged in user data to provide in response
        user_data = {}
        user_qs = get_user_model().objects.filter(email=self.request.user.email)
        if user_qs.exists():
            user_data = json.loads(serializers.serialize('json', user_qs))[0].get("fields", {})
            # remove password from user_data
            del user_data["password"]
        
        # get refresh token for the logged in user
        refresh = RefreshToken.for_user(self.request.user)
        
        # customize response
        custom_response_data = {
            "jwt_token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            "user": user_data,
            "key": key
        }
        # update original response
        original_response.data.update(custom_response_data)
        
        # return the response
        return original_response


class UserManagerViewSet(LoggingMixin, CustomViewSet):
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = get_user_model().objects.all()
    lookup_field = "slug"
    
    def get_custom_permission(self):
        if self.action in ["update"]:
            try:
                if self.get_object() == self.request.user:
                    return True
                else:
                    return False, "You are not allowed to access this content!"
            except Exception as E:
                return False, str(E)
        return True
            
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = UserUpdateSerializer
        else:
            self.serializer_class = UserSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ["update"]:
            permission_classes = [custom_permissions.GetDynamicPermissionFromViewset]
        elif self.action in ["get_logged_in_user_details"]:
            permission_classes = [custom_permissions.GetDynamicPermissionFromViewset]
        else:
            permission_classes = [custom_permissions.IsSuperUser]
        return [permission() for permission in permission_classes]
    
    def get_logged_in_user_details(self, request, *args, **kwargs):
        try:
            instance = self.request.user
            serializer = self.get_serializer(instance)
            return ResponseWrapper(data=serializer.data, msg="retrieve", status=200)
        except Exception as E:
            return ResponseWrapper(error_msg=serializer.errors if len(serializer.errors) else dict(E), msg="retrieve", error_code=400)
