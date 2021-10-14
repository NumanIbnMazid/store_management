from .serializers import (CouponSerializer, CouponUpdateSerializer, PointSettingSerializer, PointSettingUpdateSerializer)
from deals.models import Coupon, PointSetting
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import populate_related_object_id
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from rest_framework import permissions
from utils.studio_getter_helper import (
    get_studio_id_from_studio
)

class CouponManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Coupon.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_studio(selfObject=self, slug=self.kwargs.get("studio_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = CouponUpdateSerializer
        else:
            self.serializer_class = CouponSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(CouponManagerViewSet, self)._clean_data(data)
    
    def list(self, request, *args, **kwargs):
        try:
            studio_slug = kwargs.get("studio_slug")
            qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='success')
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to retrieve the list!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to retrieve the list!", error_code=400)


class PointManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = PointSetting.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_studio(selfObject=self, slug=self.kwargs.get("studio_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = PointSettingUpdateSerializer
        else:
            self.serializer_class = PointSettingSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(CouponManagerViewSet, self)._clean_data(data)
    
    def list(self, request, *args, **kwargs):
        try:
            studio_slug = kwargs.get("studio_slug")
            qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='success')
        except:
            try:
                return ResponseWrapper(error_msg=serializer.errors, msg="Failed to retrieve the list!", error_code=400)
            except Exception as E:
                return ResponseWrapper(error_msg=str(E), msg="Failed to retrieve the list!", error_code=400)

