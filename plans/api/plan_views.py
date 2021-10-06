from spaces.models import Space
from .serializers import (PlanSerializer, PlanUpdateSerializer)
from plans.models import Plan
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from rest_framework.parsers import MultiPartParser
from studios.models import Studio
from utils.helpers import ResponseWrapper


class PlanManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Plan.objects.all()
    lookup_field = "slug"
    parser_classes = (MultiPartParser, )
    
    def get_studio(self):
        try:
            return self.get_object().space.all().first().store.studio
        except Exception as E:
            space = None
            print(self.request.POST, "xxxxxxxxxxx")
            print(type(self.request.data.get("space")), "asfsdfsdsddsfsdsdfsddsff")
            if type(self.request.data.get("space")) == list or type(self.request.data.get("space")) == tuple:
                space = self.request.data.get("space")[0]
            elif type(self.request.data.get("space")) == str:
                space = self.request.data.get("space").split(",")[0]
            else:
                return ResponseWrapper(error_code=400, msg="Invalid data type received! Please input spaces and List/Array or Comma Separeted String Value!", status=400)
            print(space, "SDSDSDDasdasasdasd")
            space_qs = Space.objects.filter(id=int(space))
            if space_qs.exists():
                qs = Studio.objects.filter(id=int(space_qs.first().store.studio.id))
                if qs.exists():
                    return qs.first()
            else:
                return ResponseWrapper(error_code=400, msg="Failed to get space! Thus failed to provide required permissions required for Studio Management.", status=400)
        return ResponseWrapper(error_code=400, msg="Failed to get studio! Thus failed to provide required permissions required for Studio Management.", status=400)
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = PlanUpdateSerializer
        else:
            self.serializer_class = PlanSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(PlanManagerViewSet, self)._clean_data(data)



    
