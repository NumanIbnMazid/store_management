from .serializers import (NotificationSerializer, NotificationUpdateSerializer, NotificationPublishedSerializer)
from notifications.models import Notification
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from rest_framework.parsers import MultiPartParser

from utils.helpers import ResponseWrapper
from dateutil import parser
from studios.models import Studio

class NotificationManagerViewSet(LoggingMixin, CustomViewSet):
    
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Notification.objects.all()
    lookup_field = "slug"
    parser_classes = (MultiPartParser, )
    
    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = NotificationUpdateSerializer

        elif self.action in ["studio_notifications"]:
            self.serializer_class = NotificationPublishedSerializer
        else:
            self.serializer_class = NotificationSerializer
        return self.serializer_class
    
    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    def _clean_data(self, data):
        if isinstance(data, bytes):
            data = data.decode(errors='ignore')
        return super(NotificationManagerViewSet, self)._clean_data(data)

    
    def get_notification(self,studio_obj):
        qs = Notification.objects.filter(is_published=True, studio=studio_obj)
        notification_objects = []
        if qs.exists():
            for instance in qs:
                notification_objects.append(instance)
            return True, notification_objects
        return False, notification_objects

    
    def studio_notifications(self, request, *args, **kwargs):
        """ *** Parent Method for checking all published notification for studio *** """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            studio = int(request.data.get("studio", None))
            studio_qs = Studio.objects.filter(id=studio)
            studio_obj = None
            
            if studio_qs.exists():
                studio_obj = studio_qs.first()
            else:
                return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg=f"Studio {studio} does not exists!", status=400)

            def prepare_notification(notification_qs=None):
                notification_list = []
                for notification in notification_qs:
                    data = {}
                    data["title"] = notification.title
                    data["message"] = notification.message
                    data["published_date"] = notification.published_date
                    data["link_url"] = notification.link_url
                    data["pdf_url"] = notification.pdf_url
                    data["published_date"] = notification.published_date
                    data["published_time"] = notification.published_time
                    notification_list.append(data)
                result['notification'] = notification_list
                result['total_notification'] = len(notification_list)
                return result
            result = {
                "studio": studio,
                "notification":[]
            }

            notification_filter_result = self.get_notification(studio_obj=studio_obj)
            
            # prepare notification reponse data
            if notification_filter_result[0] == True:
                prepare_notification(notification_qs=notification_filter_result[1])
                result["notification_status"] = True
            else:
                result["notification_status"] = False
                    
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)
    

    
