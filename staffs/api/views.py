from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from .serializers import (
    StaffSerializer, StaffUpdateSerializer
)
from staffs.models import Staff
from utils.studio_getter_helper import (
    get_studio_id_from_studio
)


class StaffAccountManagerViewSet(LoggingMixin, CustomViewSet):

    logging_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    queryset = Staff.objects.all()
    lookup_field = 'slug'

    # def get_studio_id(self):
    #     return get_studio_id_from_studio(selfObject=self, slug=self.kwargs.get("studio_slug"))

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
        except Exception as E:
            return ResponseWrapper(error_msg=serializer.errors if len(serializer.errors) else dict(E), msg="create", error_code=400)

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
            return ResponseWrapper(error_msg=serializer.errors if len(serializer.errors) else dict(E), msg="update", error_code=400)

    # Dev comment-- Numan bhai how can I get studio staff I see here no relation staff with studio
    def list(self, request, *args, **kwargs):
        try:
            studio_slug = kwargs.get("studio_slug")
            qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list')
        except Exception as E:
            return ResponseWrapper(error_msg=serializer.errors if len(serializer.errors) else dict(E), msg="list", error_code=400)


