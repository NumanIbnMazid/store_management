from .business_hour_serializers import (
    StoreBusinessHourSerializer, StoreBusinessHourUpdateSerializer, BusinessHourFromWeekNameCheckerSerializer, BusinessHourFromDateCheckerSerializer
)
from stores.models import StoreBusinessHour, Store
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper, get_exception_error_msg
from utils.studio_getter_helper import (
    get_studio_id_from_store
)
from dateutil import parser


class StoreBusinessHourManagerViewSet(LoggingMixin, CustomViewSet):

    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = StoreBusinessHour.objects.all()
    lookup_field = "slug"

    def get_studio_id(self):
        return get_studio_id_from_store(selfObject=self, slug=self.kwargs.get("store_business_hours_slug"))

    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = StoreBusinessHourUpdateSerializer
        elif self.action in ["get_business_hour_from_day_of_week_name"]:
            self.serializer_class = BusinessHourFromWeekNameCheckerSerializer
        elif self.action in ["get_business_hour_from_date"]:
            self.serializer_class = BusinessHourFromDateCheckerSerializer
        else:
            self.serializer_class = StoreBusinessHourSerializer
        return self.serializer_class

    
    def get_permissions(self):
        if self.action in ["get_business_hour_from_week_name"]:
            permission_classes = [custom_permissions.IsStoreStaff, custom_permissions.StoreAccessPermission]
        else:
            permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        try:
            store_business_hours_slug = kwargs.get("store_business_hours_slug")
            qs = self.get_queryset().filter(
                store_business_hours__slug__iexact=store_business_hours_slug)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list')
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="list")
        
    def dynamic_list(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser or request.user.is_staff:
                qs = self.get_queryset()
            elif request.user.is_studio_admin:
                qs = self.get_queryset().filter(
                    store__studio__slug__iexact=request.user.studio_user.slug
                )
            elif request.user.store_moderator_user:
                qs = self.get_queryset().filter(
                    store__studio__slug__iexact=request.user.store_moderator_user.store.all()[0].studio.slug
                )
            else:
                qs = None
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance=qs, many=True)
            return ResponseWrapper(data=serializer.data, msg='list', status=200)
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="list")
        
    def get_business_hour_from_day_of_week_name(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)

            if serializer.is_valid():
                store_id = int(request.data.get("store", None))
                store_qs = Store.objects.filter(id=store_id)

                store_obj = None

                if store_qs.exists():
                    store_obj = store_qs.first()
                else:
                    return ResponseWrapper(error_code=400, error_msg=f"Store {store_id} does not exists!", msg="Failed to get the result!", status=400)
                
                day_of_week = request.data.get("day_of_week", "").title()
                
                result = {
                    "store": store_obj.name,
                    "day_of_week": day_of_week,
                    "opening_time": store_obj.store_business_hour.get_business_hour_from_day_of_week(day_of_week=day_of_week).get("opening_time", ""),
                    "closing_time": store_obj.store_business_hour.get_business_hour_from_day_of_week(day_of_week=day_of_week).get("closing_time", "")
                }
                
                return ResponseWrapper(data=result, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
                
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="Failed to get the result!")
        
    def get_business_hour_from_date(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(data=request.data, partial=True)

            if serializer.is_valid():
                store_id = int(request.data.get("store", None))
                store_qs = Store.objects.filter(id=store_id)

                store_obj = None

                if store_qs.exists():
                    store_obj = store_qs.first()
                else:
                    return ResponseWrapper(error_code=400, error_msg=f"Store {store_id} does not exists!", msg="Failed to get the result!", status=400)
                
                date_obj = parser.parse(request.data.get("date", ""))
                
                day_of_week = date_obj.strftime("%A")
                
                result = {
                    "store": store_obj.name,
                    "date": request.data.get("date", ""),
                    "day_of_week": day_of_week,
                    "opening_time": store_obj.store_business_hour.get_business_hour_from_day_of_week(day_of_week=day_of_week).get("opening_time", ""),
                    "closing_time": store_obj.store_business_hour.get_business_hour_from_day_of_week(day_of_week=day_of_week).get("closing_time", "")
                }
                
                return ResponseWrapper(data=result, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
                
        except Exception as E:
            return get_exception_error_msg(errorObj=E, msg="Failed to get the result!")
