from .serializers import (PlanSerializer, PlanUpdateSerializer)
from plans.models import Plan
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.studio_getter_helper import (
    get_studio_id_from_space
)


class PlanManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Plan.objects.all()

    def get_studio_id(self):
        return get_studio_id_from_space(selfObject=self, slug=self.kwargs.get("space_slug"))
            
    
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
