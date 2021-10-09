from .serializers import SpaceSerializer, SpaceUpdateSerializer
from spaces.models import Space
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import populate_related_object_id
from stores.models import Store


class SpaceManagerViewSet(LoggingMixin, CustomViewSet):
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Space.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        try:
            return True, self.get_object().store.studio.id
        except Exception as E:
            # get related object id
            related_object = populate_related_object_id(request=self.request, related_data_name="store")
            # check related object status
            if related_object[0] == True:
                # store queryset
                store_qs = Store.objects.filter(id=int(related_object[-1]))
                # check if store exists
                if store_qs.exists():
                    return True, store_qs.first().studio.id
                else:
                    return False, "Failed to get `Store`! Thus failed to provide required permissions for Studio Management."
            return False, related_object[-1]
    
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

    
