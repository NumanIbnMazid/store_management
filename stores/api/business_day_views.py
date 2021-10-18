from stores.models import Store, CustomBusinessDay
from utils.custom_viewset import CustomViewSet
from .business_day_serializers import (
    SingleBusinessDayCheckerSerializer, BusinessDaySerializer, YearBusinessDaysCheckerSerializer, RangeBusinessDaysCheckerSerializer
)
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
        return get_studio_id_from_store(selfObject=self, slug=self.kwargs.get("studio_slug"))
    
    def get_serializer_class(self):
        if self.action in ["check_single_business_day_status"]:
            self.serializer_class = SingleBusinessDayCheckerSerializer
        elif self.action in ["get_business_days_by_year"]:
            self.serializer_class = YearBusinessDaysCheckerSerializer
        elif self.action in ["get_business_days_by_range"]:
            self.serializer_class = RangeBusinessDaysCheckerSerializer
        else:
            self.serializer_class = BusinessDaySerializer
        return self.serializer_class
    
    def get_permissions(self):
        if self.action in ["check_single_business_day_status", "get_business_days_by_year", "get_business_days_by_range"]:
            permission_classes = [custom_permissions.IsStoreStaff]
        else:
            permission_classes = [custom_permissions.IsStudioAdmin]
        return [permission() for permission in permission_classes]
    
    
    def check_single_business_day_status(self, request, *args, **kwargs):
        """ *** Parent Method for checking Single BusinessDay *** """
        
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
                    return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg=f"Store {store_id} does not exists!", status=400)

                date_obj = parser.parse(request.data.get("date", ""))
                formatted_date_str = date_obj.strftime("%Y-%m-%d")

                result = {
                    "store": store_obj.name,
                    "type": "default_business_day",
                    "date": formatted_date_str,
                    "day_of_week": date_obj.strftime("%A"),
                    "status": "Open"
                }
                
                # get store default closed days
                store_default_closed_day_of_weeks = store_obj.default_closed_day_of_weeks
                # query in custom closed days
                store_custom_business_days = CustomBusinessDay.objects.filter(store=store_obj, date=date_obj)
                
                # check if date exists in custom business days
                if len(store_custom_business_days) >= 1:
                    # update day type for custom
                    result["type"] = store_custom_business_days.first().get_business_day_type()
                    # update status if status is closed
                    if store_custom_business_days.first().status == 0:
                        result["status"] = store_custom_business_days.first().get_status_str()
                    # update status if status is open
                    elif store_custom_business_days.first().status == 1:
                        result["status"] = store_custom_business_days.first().get_status_str()
                # check if date exists in store default closed days
                elif date_obj.strftime("%A") in store_default_closed_day_of_weeks:
                    result["type"] = "default_closed_day"
                    result["status"] = "Closed"
                # pass if do not match any conditions (result will return as it is: default result)
                else:
                    pass
                
                return ResponseWrapper(data=result, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="Failed to get the result!", error_code=400)
        
        
        
    def generate_business_day_result_from_date_range(self, start_date, end_date, store_obj):
        """[Generates Business Day Result from Date Range]

        Args:
            start_date ([DateObject]): [description]
            end_date ([DateObject]): [description]
            store_obj ([StoreObject]): [description]

        Returns:
            [Object]: [Business days]
        """
        
        business_days = []
        
        # Get store default closed day of weeks
        store_default_closed_day_of_weeks = store_obj.default_closed_day_of_weeks
        # get store custom closed days
        store_custom_closed_days = CustomBusinessDay.objects.filter(
            store=store_obj, status=0
        ).values_list("date", flat=True)
        # get store custom opening days
        store_custom_opening_days = CustomBusinessDay.objects.filter(
            store=store_obj, status=1
        ).values_list("date", flat=True)

        # define timedelta
        time_delta = datetime.timedelta(days=1)

        while start_date <= end_date:
            # check if date exists in store custom business days
            if start_date in store_custom_closed_days:
                # prepare custom business day data
                business_day_data = {
                    "type": "custom_closed_day",
                    "date": start_date.strftime("%Y-%m-%d"),
                    "day_of_week": start_date.strftime("%A"),
                    "status": "Closed"
                }
                # insert business day data in business_days
                business_days.append(business_day_data)
            elif start_date in store_custom_opening_days:
                is_exists = start_date.strftime(
                    "%A") in store_default_closed_day_of_weeks
                if is_exists:
                    # prepare default business day data
                    business_day_data = {
                        "type": "custom_business_day",
                        "date": start_date.strftime("%Y-%m-%d"),
                        "day_of_week": start_date.strftime("%A"),
                        "status": "Open"
                    }
                    # insert business day data in business_days
                    business_days.append(business_day_data)
            elif start_date.strftime("%A") in store_default_closed_day_of_weeks:
                is_exists = start_date.strftime(
                    "%A") in store_default_closed_day_of_weeks
                if is_exists:
                    # prepare default business day data
                    business_day_data = {
                        "type": "default_closed_day",
                        "date": start_date.strftime("%Y-%m-%d"),
                        "day_of_week": start_date.strftime("%A"),
                        "status": "Closed"
                    }
                    # insert business day data in business_days
                    business_days.append(business_day_data)
            else:
                # prepare default business day data
                business_day_data = {
                    "type": "default_business_day",
                    "date": start_date.strftime("%Y-%m-%d"),
                    "day_of_week": start_date.strftime("%A"),
                    "status": "Open"
                }
                # insert business day data in business_days
                business_days.append(business_day_data)

            # Increment Start Date
            start_date += time_delta
            
        return business_days
    
    
    def get_business_days_by_year(self, request, *args, **kwargs):
        """ *** Parent Method for getting business days by year *** """
        
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
                    return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg=f"Store {store_id} does not exists!", status=400)

                year = request.data.get("year", None)

                result = {
                    "store": store_obj.name,
                    "year": year,
                    "business_days": []
                }

                start_date = datetime.date(int(year), 1, 1)
                end_date = datetime.date(int(year), 12, 31)
                
                business_days = self.generate_business_day_result_from_date_range(start_date=start_date, end_date=end_date, store_obj=store_obj)
                
                result["business_days"] = business_days

                return ResponseWrapper(data=result, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="Failed to get the result!", error_code=400)
    
    
    def get_business_days_by_range(self, request, *args, **kwargs):
        """ *** Parent Method for getting business days by year *** """
        
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
                    return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg=f"Store {store_id} does not exists!", status=400)

                start_date = request.data.get("start_date", None)
                end_date = request.data.get("end_date", None)
                
                start_date_obj = parser.parse(start_date)
                end_date_obj = parser.parse(end_date)

                result = {
                    "store": store_obj.name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "business_days": []
                }

                business_days = self.generate_business_day_result_from_date_range(
                    start_date=start_date_obj, end_date=end_date_obj, store_obj=store_obj
                )
                
                result["business_days"] = business_days

                return ResponseWrapper(data=result, status=200)
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
        
        except AttributeError as E:
            return ResponseWrapper(error_msg=str(E), msg="Failed to get the result!", error_code=400)
