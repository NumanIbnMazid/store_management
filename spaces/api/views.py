from .serializers import SpaceSerializer, SpaceUpdateSerializer, SpaceListSerializer
from spaces.models import Space
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import populate_related_object_id
from stores.models import Store
from utils.helpers import ResponseWrapper
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
        elif self.action in ['list']:
            self.serializer_class = SpaceListSerializer
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
    
    def list(self, request, *args, **kwargs):
        try:
            store_slug = kwargs.get("store_slug")
            qs = self.get_queryset().filter(store__slug__iexact=store_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='success')
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to retrieve the list!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to retrieve the list!", error_code=400)

    
