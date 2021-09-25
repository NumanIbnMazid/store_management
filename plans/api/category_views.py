from .serializers import (CategorySerializer, CategoryUpdateSerializer)
from plans.models import Category
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet

class CategoryManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Category.objects.all()
    lookup_field = "slug"
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = CategoryUpdateSerializer
        else:
            self.serializer_class = CategorySerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
