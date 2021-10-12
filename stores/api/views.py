from .serializers import (
    StoreSerializer, StoreUpdateSerializer, CustomClosedDaySerializer, CustomClosedDayUpdateSerializer
)
from stores.models import Store, CustomClosedDay
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from utils.studio_getter_helper import (
    get_studio_id_from_studio, get_studio_id_from_store
)

class StoreManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Store.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_studio(selfObject=self, slug=self.kwargs.get("studio_slug"))
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = StoreUpdateSerializer
        else:
            self.serializer_class = StoreSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        studio_slug = kwargs.get("studio_slug")
        qs = self.get_queryset().filter(studio__slug__iexact=studio_slug)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, msg='success')
    
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(StoreManagerViewSet, self)._clean_data(data)


class CustomClosedDayManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = CustomClosedDay.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_store(selfObject=self)
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = CustomClosedDayUpdateSerializer
        else:
            self.serializer_class = CustomClosedDaySerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            date = request.data.get("date", None)
            store_custom_closed_day_qs = CustomClosedDay.objects.filter(
                date=date, store=self.get_object().store
            ).exclude(slug__iexact=kwargs["slug"])
            if store_custom_closed_day_qs.exists():
                error_message = f"Date `{date}` already exists!"
                return ResponseWrapper(error_code=400, error_msg=error_message, msg="Failed to update!", status=400)
            qs = serializer.update(instance=self.get_object(), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)
