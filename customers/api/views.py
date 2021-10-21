from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import permissions
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper, get_exception_error_msg
from .serializers import (
    CustomerSerializer, CustomerUpdateSerializer
)
from customers.models import Customer


class AccountManagerViewSet(LoggingMixin, CustomViewSet):
    logging_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    queryset = Customer.objects.all()
    lookup_field = 'slug'

    def get_custom_permission(self):
        if self.action in ["create"]:
            return True
        else:
            try:
                if self.get_object().user == self.request.user:
                    return True
            except Exception as E:
                return False, str(E)
        return False, "You are not allowed to access this content!"

    def get_serializer_class(self):
        if self.action in ["create"]:
            self.serializer_class = CustomerSerializer

        elif self.action in ["update"]:
            self.serializer_class = CustomerUpdateSerializer

        elif self.action in ["list"]:
            self.serializer_class = CustomerSerializer

        else:
            self.serializer_class = CustomerSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [permissions.AllowAny]

        elif self.action in ["list"]:
            permission_classes = [custom_permissions.IsSuperUser]
            
        else:
            permission_classes = [custom_permissions.GetDynamicPermissionFromViewset]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                user_instance = serializer.save_base_user(request)
                customer_instance = serializer.save(user=user_instance)
                return ResponseWrapper(data=serializer.data, status=200)
            return ResponseWrapper(error_code=400, error_msg=serializer.errors)
        except Exception as E:
            return ResponseWrapper(error_msg=get_exception_error_msg(errorObj=E), msg="create", error_code=400)

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
        except Exception as E:
            return ResponseWrapper(error_msg=get_exception_error_msg(errorObj=E), msg="update", error_code=400)


     

     
