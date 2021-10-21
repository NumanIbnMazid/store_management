from .serializers import (CurrencySerializer, CurrencyUpdateSerializer)
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from studios.models import Currency
from utils.helpers import ResponseWrapper, get_exception_error_msg
from utils.studio_getter_helper import (
    get_studio_id_from_studio
)
from django.db.models import Q

"""
    ----------------------- * Currency * -----------------------
"""

class CurrencyManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Currency.objects.all()
    lookup_field = "slug"

    def get_studio_id(self):
        return get_studio_id_from_studio(selfObject=self, slug=self.kwargs.get("studio_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = CurrencyUpdateSerializer
        else:
            self.serializer_class = CurrencySerializer
        return self.serializer_class
    
    def get_permissions(self):
        if self.action in ["dynamic_list"]:
            permission_classes = [custom_permissions.IsStudioStaff]
        else:
            permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(CurrencyManagerViewSet, self)._clean_data(data)

    
    def list(self, request, *args, **kwargs):
        try:
            studio_slug = kwargs.get("studio_slug")
            qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list', status=200)
        except Exception as E:
            return ResponseWrapper(error_msg=get_exception_error_msg(errorObj=E), msg="list", error_code=400)

   

   

    
    
