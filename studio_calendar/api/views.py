from datetime import date
from studios.models import Studio
import holidays
from .serializers import StudioCalendarSerializer, StudioCalendarUpdateSerializer, SingleHolidayCheckerSerializer, RangeHolidayCheckerSerializer
from studio_calendar.models import StudioCalendar
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from dateutil import parser


class StudioCalendarManagerViewSet(LoggingMixin, CustomViewSet):

    logging_methods = ["GET", "POST", "PATCH", "DELETE"]
    queryset = StudioCalendar.objects.all()
    lookup_field = "slug"
    
    # define Japan Holiday
    jp_holidays = holidays.JP()
    # define base holiday
    base_holidays = holidays.HolidayBase()

    def get_serializer_class(self):
        if self.action in ["update"]:
            self.serializer_class = StudioCalendarUpdateSerializer
        elif self.action in ["check_single_holiday"]:
            self.serializer_class = SingleHolidayCheckerSerializer
        elif self.action in ['check_holiday_between_range']:
            self.serializer_class = RangeHolidayCheckerSerializer
        else:
            self.serializer_class = StudioCalendarSerializer
        return self.serializer_class

    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioStaff]
        return [permission() for permission in permission_classes]
    
    def create_studio_holidays_for_year(self, year, studio_obj):
        try:
            for date, name in sorted(holidays.JP(years=int(year)).items()):
                # print(date, name)
                StudioCalendar.objects.create(studio=studio_obj, year=year, date=date, title=name)
            return True
        except Exception as E:
            raise Exception(f"Failed to create holidays for year {year}. Exception: {str(E)}")
    
    def check_studio_holidays_exists_for_year(self, year, studio_obj):
        qs = StudioCalendar.objects.filter(year=year, studio=studio_obj)
        if qs.exists():
            return True
        return False
    
    def get_single_holiday(self, date, studio_obj):
        date_obj = parser.parse(date)
        year = date_obj.year
        qs = StudioCalendar.objects.filter(year=year, date=date_obj, studio=studio_obj)
        if qs.exists():
            return True, qs.first()
        return False, None
    
    def get_holiday_from_range(self, start_date, end_date, studio_obj):
        date_start = parser.parse(start_date)
        end_start = parser.parse(end_date)
        
        start_year = date_start.year
        end_year = date_start.year

        qs = StudioCalendar.objects.filter(year=start_year, date__range=[date_start,end_start], studio=studio_obj)
        date_obj = []
        if qs.exists():
            for instance in qs:
                date_obj.append((True, instance))
            return date_obj
        else:
            date_obj.append((False, None))
            return date_obj

    # def get_holiday_from_list():

    # def get_holidays_for_year():
        
    
    def check_single_holiday(self, request, *args, **kwargs):
        """ *** Parent Method for checking Single Holiday *** """
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
            
            date_obj = parser.parse(request.data.get("date", ""))
            year = date_obj.year
            formatted_date_str = date_obj.strftime("%Y-%m-%d")
            
            result = {
                "date": formatted_date_str,
                "studio": studio,
                "is_holiday": None,
                "holiday": {}
            }
            
            def prepare_holiday_data(holiday_instance=None):
                result["is_holiday"] = True
                result["holiday"]["title"] = holiday_instance.title
                result["holiday"]["comments"] = holiday_instance.comments
                result["holiday"]["country_code"] = holiday_instance.country_code
                result["holiday"]["year"] = holiday_instance.year
                return result
            
            # check if studio holidays exists
            holiday_existance_result = self.check_studio_holidays_exists_for_year(year=year, studio_obj=studio_obj)
            if holiday_existance_result == True:
                holiday_filter_result = self.get_single_holiday(date=formatted_date_str, studio_obj=studio_obj)
                if holiday_filter_result[0] == True:
                    prepare_holiday_data(holiday_instance=holiday_filter_result[1])
                else:
                    result["is_holiday"] = False
            else:
                self.create_studio_holidays_for_year(year=str(year), studio_obj=studio_obj)
                holiday_filter_result = self.get_single_holiday(date=formatted_date_str, studio_obj=studio_obj)
                if holiday_filter_result[0] == True:
                    prepare_holiday_data(holiday_instance=holiday_filter_result[1])
                else:
                    result["is_holiday"] = False
                    
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)
    
    def check_holiday_between_range(self, request, *args, **kwargs):
        """ *** Parent Method for checking holiday between range *** """
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
            
            start_date = parser.parse(request.data.get("start_date", ""))
            start_year = start_date.year
            formatted_start_date_str = start_date.strftime("%Y-%m-%d")

            end_date = parser.parse(request.data.get("end_date", ""))
            end_year = end_date.year
            formatted_end_date_str = end_date.strftime("%Y-%m-%d")
            
            result = {
                "start_date": formatted_start_date_str,
                "end_date": formatted_end_date_str,
                "studio": studio,
                "is_holiday":None,
                "data":{}
            }
            
            def prepare_holiday_data(holiday_instance=None):
                instance_list = []
                for instance in holiday_instance:
                    data = {
                    "holiday": {}
                    }
                    instance_field = instance[1]
                    data["holiday"]["title"] = instance_field.title
                    data["holiday"]["comments"] = instance_field.comments
                    data["holiday"]["country_code"] = instance_field.country_code
                    data["holiday"]["year"] = instance_field.year
                    data["holiday"]["date"] = instance_field.date
                    data["holiday"]["is_holiday"] = True
                    instance_list.append(data)
                result['data']=instance_list
                result['is_holiday']=True
                return result
            
            # check if studio holidays exists
            holiday_existance_result_for_start = self.check_studio_holidays_exists_for_year(year=start_year, studio_obj=studio_obj)
            holiday_existance_result_for_end = self.check_studio_holidays_exists_for_year(year=end_year, studio_obj=studio_obj)

            if holiday_existance_result_for_start == True and holiday_existance_result_for_end == True:
                holiday_filter_result = self.get_holiday_from_range(start_date=formatted_start_date_str, end_date=formatted_end_date_str, studio_obj=studio_obj)
                for instance in holiday_filter_result:
                    if instance[0] == True:
                        prepare_holiday_data(holiday_instance=holiday_filter_result)
                    else:
                        result["is_holiday"] = False 
            else:
                self.create_studio_holidays_for_year(year=str(start_year), studio_obj=studio_obj)
                self.create_studio_holidays_for_year(year=str(end_year), studio_obj=studio_obj)
                holiday_filter_result = self.get_holiday_from_range(start_date=formatted_start_date_str, end_date=formatted_end_date_str, studio_obj=studio_obj)
                for instance in holiday_filter_result:
                    if instance[0] == True:
                        prepare_holiday_data(holiday_instance=holiday_filter_result)
                    else:
                        result["is_holiday"] = False 
                    
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)

# def check_holiday_from_list():
# def check_holidays_for_year():
