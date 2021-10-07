from .serializers import (OptionSerializer, OptionUpdateSerializer)
from plans.models import Option, OptionCategory
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from rest_framework.parsers import MultiPartParser
from studios.models import Studio
from utils.helpers import ResponseWrapper

class OptionManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Option.objects.all()
    lookup_field = "slug"
    parser_classes = (MultiPartParser, )
    
    def get_studio(self):
        try:
            return self.get_object().option_category.studio
        except Exception as E:
            option_category_qs = OptionCategory.objects.filter(id=self.request.data.get("option_category"))
            if option_category_qs.exists():
                qs = Studio.objects.filter(id=int(option_category_qs.first().studio.id))
                if qs.exists():
                    return qs.first()
            else:
                return ResponseWrapper(error_code=400, msg="Failed to get Option Category! Thus failed to provide required permissions required for Studio Management.", status=400)
        return ResponseWrapper(error_code=400, msg="Failed to get studio! Thus failed to provide required permissions required for Studio Management.", status=400)
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = OptionUpdateSerializer
        else:
            self.serializer_class = OptionSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(OptionManagerViewSet, self)._clean_data(data)

