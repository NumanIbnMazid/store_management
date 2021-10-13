from stores.models import Store, CustomClosedDay
from utils.custom_viewset import CustomViewSet
from .business_day_serializers import SingleBusinessDayCheckerSerializer, BusinessDaySerializer
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.helpers import ResponseWrapper
from utils.studio_getter_helper import get_studio_id_from_store
import datetime
from dateutil import parser


class BusinessDayManagerViewSet(CustomViewSet):
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = Store.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        return get_studio_id_from_store(selfObject=self)
    
    def get_serializer_class(self):
        if self.action in ["check_single_business_day_status"]:
            self.serializer_class = SingleBusinessDayCheckerSerializer
        else:
            self.serializer_class = BusinessDaySerializer
        return self.serializer_class
    
    def get_permissions(self):
        if self.action in ["check_single_business_day_status"]:
            permission_classes = [custom_permissions.IsStudioStaff]
        else:
            permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    
    def check_single_business_day_status(self, request, *args, **kwargs):
        """ *** Parent Method for checking Single BusinessDay *** """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)

        if serializer.is_valid():
            store_id = int(request.data.get("store", None))
            store_qs = Store.objects.filter(id=store_id)

            store_obj = None

            if store_qs.exists():
                store_obj = store_qs.first()
            else:
                return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg=f"Store {store_id} does not exists!", status=400)

            date_obj = parser.parse(request.data.get("date", ""))
            year = date_obj.year
            formatted_date_str = date_obj.strftime("%Y-%m-%d")

            result = {
                "store": store_obj.name,
                "type": "default_business_day",
                "date": formatted_date_str,
                "day_name": date_obj.strftime("%A"),
                "status": "Open"
            }
            
            def prepare_business_day_data(is_custom=False):

                result["store"] = store_obj.name
                result["type"] = "custom_closed_day" if is_custom == True else "default_closed_day"
                result["day_name"] = date_obj.strftime("%A")
                result["status"] = "Closed"

                return result
            
            # check if date exists in store custom closed days
            qs = CustomClosedDay.objects.filter(store=store_obj, date=date_obj)
            if qs:
                # prepare custom business day data
                prepare_business_day_data(is_custom=True)
            else:
                store_default_closed_days = store_obj.default_closed_days
                is_exists = date_obj.strftime("%A") in store_default_closed_days
                if is_exists:
                    # prepare default business day data
                    prepare_business_day_data()
            
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)
