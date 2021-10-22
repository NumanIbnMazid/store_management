from .serializers import (StoreBusinessHourSerializer, StoreBusinessHourUpdateSerializer)
from stores.models import StoreBusinessHour
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper, get_exception_error_msg
from utils.studio_getter_helper import (
    get_studio_id_from_store
)


class StoreBusinessHourManagerViewSet(LoggingMixin, CustomViewSet):

    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = StoreBusinessHour.objects.all()
    lookup_field = "slug"

    def get_studio_id(self):
        return get_studio_id_from_store(selfObject=self, slug=self.kwargs.get("store_business_hours_slug"))

    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = StoreBusinessHourUpdateSerializer
        else:
            self.serializer_class = StoreBusinessHourSerializer
        return self.serializer_class

    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin,
                              custom_permissions.StoreAccessPermission]
        return [permission() for permission in permission_classes]  

    def list(self, request, *args, **kwargs):
        try:
            store_business_hours_slug = kwargs.get("store_business_hours_slug")
            qs = self.get_queryset().filter(
                store_business_hours__slug__iexact=store_business_hours_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list')
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="list")
