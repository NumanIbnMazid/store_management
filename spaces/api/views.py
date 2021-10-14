from .serializers import SpaceSerializer, SpaceUpdateSerializer
from spaces.models import Space
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.studio_getter_helper import (
    get_studio_id_from_store
)


class SpaceManagerViewSet(LoggingMixin, CustomViewSet):
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Space.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_store(selfObject=self, slug=self.kwargs.get("store_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = SpaceUpdateSerializer
        else:
            self.serializer_class = SpaceSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(SpaceManagerViewSet, self)._clean_data(data)

    
