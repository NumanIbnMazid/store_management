from stores.models import Store
from .business_day_serializers import SingleBusinessDayCheckerSerializer, BusinessDaySerializer
from studio_calendar.models import BusinessDay
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from dateutil import parser
import datetime
from utils.helpers import populate_related_object_id


class BusinessDayManagerViewSet(LoggingMixin, CustomViewSet):
    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = BusinessDay.objects.all()
    lookup_field = "slug"
    
    def get_studio_id(self):
        try:
            return True, self.get_object().store.studio.id
        except Exception as E:
            # get related object id
            related_object = populate_related_object_id(request=self.request, related_data_name="store")
            # check related object status
            if related_object[0] == True:
                # store queryset
                store_qs = Store.objects.filter(id=int(related_object[-1]))
                # check if store exists
                if store_qs.exists():
                    return True, store_qs.first().studio.id
                else:
                    return False, "Failed to get `Store`! Thus failed to provide required permissions for Studio Management."
            return False, related_object[-1]
        
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
    
    def create_business_days_for_year(self, year, store_obj):
        
        try:
            start_date = datetime.date(int(year), 1, 1)
            end_date = datetime.date(int(year), 12, 31)

            time_delta = datetime.timedelta(days=1)

            while start_date <= end_date:
                # Create BusinessDay Object
                day_name = start_date.strftime("%A")
                BusinessDay.objects.create(
                    store=store_obj, date=start_date, day_name=day_name, status=0 if day_name in store_obj.default_closed_days else 1
                )
                start_date += time_delta
            return True
        
        except Exception as E:
            raise Exception(f"Failed to create holidays for year {year}. Exception: {str(E)}")
    
    def check_business_days_exists_for_year(self, year, store_obj):
        qs = BusinessDay.objects.filter(date__year__iexact=str(year), store=store_obj)
        if qs.exists():
            return True
        return False
    
    def get_single_business_day(self, date, store_obj):
        date_obj = parser.parse(date)
        qs = BusinessDay.objects.filter(date=date_obj, store=store_obj)
        if qs.exists():
            return True, qs.first()
        return False, None
    
    def get_business_days_from_range(self, start_date, end_date, store_obj):
        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)
        
        start_year = start_date.year
        end_year = end_date.year

        qs = BusinessDay.objects.filter(date__year__range=[start_year, end_year], date__range=[start_date, end_date], store=store_obj)
        business_day_objects = []
        if qs.exists():
            for instance in qs:
                business_day_objects.append(instance)
            return True, business_day_objects
        return False, business_day_objects
    
    def get_business_days_for_year(self, year, store_obj):
        qs = BusinessDay.objects.filter(date__year__iexact=str(year), store=store_obj)
        business_day_objects = []
        if qs.exists():
            for instance in qs:
                business_day_objects.append(instance)
            return True, business_day_objects
        return False, business_day_objects
    
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
                "slug": None,
                "date": formatted_date_str,
                "day_name": None,
                "status": None,
                "created_at": None,
                "updated_at": None
            }

            def prepare_business_day_data(business_day_instance=None):
                
                result["store"] = business_day_instance.store.name
                result["slug"] = business_day_instance.slug
                result["date"] = business_day_instance.date
                result["day_name"] = business_day_instance.day_name
                result["status"] = business_day_instance.get_status_str()
                result["created_at"] = business_day_instance.created_at
                result["updated_at"] = business_day_instance.updated_at
                
                return result

            # check if studio business day exists
            business_day_existance_result = self.check_business_days_exists_for_year(year=year, store_obj=store_obj)

            # create business days for a year if not exists
            if not business_day_existance_result == True:
                self.create_business_days_for_year(year=str(year), store_obj=store_obj)

            # get holiday from DB
            business_day_filter_result = self.get_single_business_day(date=formatted_date_str, store_obj=store_obj)

            # preapare holiday result data
            if business_day_filter_result[0] == True:
                prepare_business_day_data(business_day_instance=business_day_filter_result[1])

            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)
