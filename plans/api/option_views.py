from .serializers import (OptionSerializer, OptionUpdateSerializer)
from plans.models import Option
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper, get_exception_error_msg
from utils.studio_getter_helper import (
    get_studio_id_from_option_category
)
from django.db.models import Q

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
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="list")
        
    def dynamic_list(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser or request.user.is_staff:
                qs = self.get_queryset()
            elif request.user.is_studio_admin or request.user.is_store_staff:
                qs = self.get_queryset().filter(
                    Q(option_category__studio__slug__iexact=request.user.studio_user.slug) |
                    Q(option_category__studio__slug__iexact=request.user.store_moderator_user.store.all()[0].studio.slug)
                )
            else:
                qs = None
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list', status=200)
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="list")

