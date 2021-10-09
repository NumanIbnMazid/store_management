from spaces.models import Space
from .serializers import (PlanSerializer, PlanUpdateSerializer)
from plans.models import Plan
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from studios.models import Studio
from utils.helpers import populate_related_object_id


class PlanManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Plan.objects.all()
    lookup_field = "slug"
    
    def get_studio(self):
        try:
            return True, self.get_object().space.all().first().store.studio
        except Exception as E:
            # get related object id
            related_object = populate_related_object_id(request=self.request, related_data_name="space")
            # check related object status
            if related_object[0] == False:
                return False, related_object[-1]
            # space queryset
            space_qs = Space.objects.filter(id=int(related_object[-1]))
            # check if space is exists
            if space_qs.exists():
                qs = Studio.objects.filter(id=int(space_qs.first().store.studio.id))
                if qs.exists():
                    return True, qs.first()
            else:
                return False, "Failed to get `Space`! Thus failed to provide required permissions required for Studio Management."
            
        return False, "Failed to get `Studio`! Thus failed to provide required permissions required for Studio Management."
    
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = PlanUpdateSerializer
        else:
            self.serializer_class = PlanSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [
            custom_permissions.IsStudioAdmin, custom_permissions.SpaceAccessPermission, custom_permissions.OptionAccessPermission
        ]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(PlanManagerViewSet, self)._clean_data(data)