from .serializers import (OptionSerializer, OptionUpdateSerializer)
from plans.models import Option, OptionCategory
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import populate_related_object_id

class OptionManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Option.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        try:
            return True, self.get_object().option_category.studio.id
        except Exception as E:
            # get related object id
            related_object = populate_related_object_id(request=self.request, related_data_name="option_category")
            # check related object status
            if related_object[0] == True:
                # query option category
                option_category_qs = OptionCategory.objects.filter(id=int(related_object[-1]))
                if option_category_qs.exists():
                    return True, option_category_qs.first().studio.id
                else:
                    return False, "Failed to get `OptionCategory`! Thus failed to provide required permissions for Studio Management."
            return False, related_object[-1]
    
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

