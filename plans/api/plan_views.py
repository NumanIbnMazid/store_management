from .serializers import (PlanSerializer, PlanUpdateSerializer)
from plans.models import Plan
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
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
    
    def create(self, request):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                qs = serializer.save()
                serializer = self.serializer_class(instance=qs)
                return ResponseWrapper(data=serializer.data, msg="create", status=200)
            return ResponseWrapper(error_msg=serializer.errors, msg="create", error_code=400)
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="create", error_code=400)
    
    def list(self, request, *args, **kwargs):
        try:
            space_slug = kwargs.get("space_slug")
            qs = self.get_queryset().filter(space__slug__iexact=space_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list')
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="list", error_code=400)

