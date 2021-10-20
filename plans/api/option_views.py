from .serializers import (OptionSerializer, OptionUpdateSerializer)
from plans.models import Option
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from utils.studio_getter_helper import (
    get_studio_id_from_option_category
)

class OptionManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Option.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_option_category(selfObject=self, slug=self.kwargs.get("option_category_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = OptionUpdateSerializer
        else:
            self.serializer_class = OptionSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin,
                              custom_permissions.OptionAccessPermission]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(OptionManagerViewSet, self)._clean_data(data)
    
    def list(self, request, *args, **kwargs):
        try:
            option_category_slug = kwargs.get("option_category_slug")
            qs = self.get_queryset().filter(option_category__slug__iexact=option_category_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list')
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="list", error_code=400)

