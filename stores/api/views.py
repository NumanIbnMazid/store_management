from .serializers import (
    StoreSerializer, StoreUpdateSerializer, CustomClosedDaySerializer, CustomClosedDayUpdateSerializer
)
from stores.models import Store, CustomClosedDay
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import populate_related_object_id
from utils.helpers import ResponseWrapper
from utils.studio_getter_helper import (
    get_studio_id_from_studio, get_studio_id_from_store
)

class StoreManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Store.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        try:
            return True, self.get_object().studio.id
        except Exception as E:
            # get related object id
            related_object = populate_related_object_id(request=self.request, related_data_name="studio")
            # check related object status
            if related_object[0] == True:
                return True, related_object[-1]
            return False, related_object[-1]
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = StoreUpdateSerializer
        else:
            self.serializer_class = StoreSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        studio_slug = kwargs.get("studio_slug")
        qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, msg='success')
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(StoreManagerViewSet, self)._clean_data(data)


class CustomClosedDayManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = CustomClosedDay.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_store(selfObject=self)
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = CustomClosedDayUpdateSerializer
        else:
            self.serializer_class = CustomClosedDaySerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]