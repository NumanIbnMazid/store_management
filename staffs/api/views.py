from rest_framework.decorators import permission_classes
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import permissions, status
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from .serializers import (
    StaffSerializer, StaffUpdateSerializer
)
from staffs.models import Staff


class StaffAccountManagerViewSet(LoggingMixin, CustomViewSet):

    logging_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    queryset = Staff.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ["create"]:
            self.serializer_class = StaffSerializer
        if self.action in ["update"]:
            self.serializer_class = StaffUpdateSerializer
        else:
            self.serializer_class = StaffSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action in ["create", "update"]:
            permission_classes = [custom_permissions.IsSuperUser]
        else:
            permission_classes = [custom_permissions.IsStaff]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                user_instance = serializer.save_base_user(request)
                staff_instance = serializer.save(user=user_instance)
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
                qs.user.name = request.data.get('user', {}).get("name", None)
                qs.user.save()
                return ResponseWrapper(data=serializer.data, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to update!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to update!", error_code=400)
