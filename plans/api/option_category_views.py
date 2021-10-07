from studios.models import Studio
from .serializers import (OptionCategorySerializer, OptionCategoryUpdateSerializer)
from plans.models import OptionCategory
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from rest_framework.parsers import MultiPartParser
from utils.helpers import ResponseWrapper

class OptionCategoryManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = OptionCategory.objects.all()
    lookup_field = "slug"
    parser_classes = (MultiPartParser, )
    
    def get_studio(self):
        try:
            return self.get_object().studio
        except Exception as E:
            qs = Studio.objects.filter(id=int(self.request.data.get("studio")))
            if qs.exists():
                return qs.first()
        return ResponseWrapper(error_code=400, msg="Failed to get studio! Thus failed to provide required permissions required for Studio Management.", status=400)
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = OptionCategoryUpdateSerializer
        else:
            self.serializer_class = OptionCategorySerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(OptionCategoryManagerViewSet, self)._clean_data(data)


# if self.action in ["destroy"]:
#     print(self.request, "DATATATATATATATA", self.request, "REREREREER")
#     slug = self.request.data.get("slug", None)
#      print(slug, "SSSLLLUUGGG")
#       qs = OptionCategory.objects.filter(slug__iexact=slug)
#        print(qs, "QQQQSSSS")
#         if qs.exists():
#              studio = qs.first().studio
#               print(studio, "SSSSSS", self.request.user,
#                      "RRRRRUUUU", studio.user, "SSSSSSUUUUUUU")
#                if studio.user == self.request.user:
#                     pass
#                 else:
#                     raise Exception("Permission Denied!")
