from datetime import date
from studios.models import Studio
import holidays
from .serializers import (
    StudioCalendarSerializer, StudioCalendarUpdateSerializer, SingleHolidayCheckerSerializer, RangeHolidayCheckerSerializer, YearHolidayCheckerSerializer, ListHolidayCheckerSerializer
)
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
        elif self.action in ['check_holidays_for_year']:
            self.serializer_class = YearHolidayCheckerSerializer
        elif self.action in ['check_holidays_from_list']:
            self.serializer_class = ListHolidayCheckerSerializer
        elif self.action in ["create"]:
            self.serializer_class = StudioCalendarSerializer
        elif self.action in ["update"]:
            self.serializer_class = StudioCalendarUpdateSerializer
        elif self.action in ["destroy"]:
            self.serializer_class = StudioCalendarUpdateSerializer
        else:
            self.serializer_class = StudioCalendarSerializer

        return self.serializer_class

    def get_permissions(self):
        permission_classes = [custom_permissions.IsStudioStaff]
        return [permission() for permission in permission_classes]
    
    def create_studio_holidays_for_year(self, year, studio_obj):
        try:
            for date, name in sorted(holidays.JP(years=int(year)).items()):
                StudioCalendar.objects.create(studio=studio_obj, year=year, date=date, title=name)
            return True
        except Exception as E:
            raise Exception(f"Failed to create holidays for year {year}. Exception: {str(E)}")
    
    def check_studio_holidays_exists_for_year(self, year, studio_obj):
        qs = StudioCalendar.objects.filter(year__iexact=str(year), studio=studio_obj)
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
    
    def get_holidays_from_range(self, start_date, end_date, studio_obj):
        start_date = parser.parse(start_date)
        end_date = parser.parse(end_date)
        
        start_year = start_date.year
        end_year = end_date.year

        qs = StudioCalendar.objects.filter(year__range=[start_year, end_year], date__range=[start_date, end_date], studio=studio_obj)
        holiday_objects = []
        if qs.exists():
            for instance in qs:
                holiday_objects.append(instance)
            return True, holiday_objects
        return False, holiday_objects
    
    def get_holidays_for_year(self, year, studio_obj):
        qs = StudioCalendar.objects.filter(year=str(year), studio=studio_obj)
        holiday_objects = []
        if qs.exists():
            for instance in qs:
                holiday_objects.append(instance)
            return True, holiday_objects
        return False, holiday_objects

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
                "is_holiday": False,
                "holiday": {}
            }
            
            def prepare_holiday_data(holiday_instance=None):
                result["holiday"]["title"] = holiday_instance.title
                result["holiday"]["comments"] = holiday_instance.comments
                result["holiday"]["country_code"] = holiday_instance.country_code
                result["holiday"]["year"] = holiday_instance.year
                return result
            
            # check if studio holidays exists
            holiday_existance_result = self.check_studio_holidays_exists_for_year(year=year, studio_obj=studio_obj)
            
            # create holidays for a year if not exists
            if not holiday_existance_result == True:
                self.create_studio_holidays_for_year(year=str(year), studio_obj=studio_obj)
            
            # get holiday from DB
            holiday_filter_result = self.get_single_holiday(date=formatted_date_str, studio_obj=studio_obj)
            
            # preapare holiday result data
            if holiday_filter_result[0] == True:
                prepare_holiday_data(holiday_instance=holiday_filter_result[1])
                result["is_holiday"] = True
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
                "is_holiday": False,
                "total_holidays": 0,
                "holidays": []
            }
            
            def prepare_holiday_data(holiday_qs=None):
                holiday_list = []
                for holiday in holiday_qs:
                    data = {}
                    data["title"] = holiday.title
                    data["comments"] = holiday.comments
                    data["country_code"] = holiday.country_code
                    data["year"] = holiday.year
                    data["date"] = holiday.date
                    holiday_list.append(data)
                result['holidays'] = holiday_list
                result['total_holidays'] = len(holiday_list)
                return result
            
            # check if studio holidays exists for start and end year
            holiday_existance_result_for_start = self.check_studio_holidays_exists_for_year(year=start_year, studio_obj=studio_obj)
            holiday_existance_result_for_end = self.check_studio_holidays_exists_for_year(year=end_year, studio_obj=studio_obj)
            
            # Create holidays for year if not exists
            if not holiday_existance_result_for_start == True:
                self.create_studio_holidays_for_year(year=str(start_year), studio_obj=studio_obj)
            
            if not start_year == end_year and not holiday_existance_result_for_end == True:
                self.create_studio_holidays_for_year(year=str(end_year), studio_obj=studio_obj)

            # filter holidays between date range
            holiday_filter_result = self.get_holidays_from_range(start_date=formatted_start_date_str, end_date=formatted_end_date_str, studio_obj=studio_obj)
            
            # prepare holiday response data
            if holiday_filter_result[0] == True:
                prepare_holiday_data(holiday_qs=holiday_filter_result[1])
                result["is_holiday"] = True
            else:
                result["is_holiday"] = False
                    
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)


    def check_holidays_for_year(self, request, *args, **kwargs):
        """ *** Parent Method for checking all holidays of the year *** """
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
            
            year = request.data.get("year", "")
            result = {
                "year":year,
                "studio": studio,
                "is_holiday": False,
                "total_holidays": 0,
                "holidays": []
            }
            
            def prepare_holiday_data(holiday_qs=None):
                holiday_list = []
                for holiday in holiday_qs:
                    data = {}
                    data["title"] = holiday.title
                    data["comments"] = holiday.comments
                    data["country_code"] = holiday.country_code
                    data["year"] = holiday.year
                    data["date"] = holiday.date
                    holiday_list.append(data)
                result['holidays'] = holiday_list
                result['total_holidays'] = len(holiday_list)
                return result
            
            # check if studio holidays exists for year
            holiday_existance_result_for_year = self.check_studio_holidays_exists_for_year(year=year, studio_obj=studio_obj)

            # create holidays for year if not exists
            if not holiday_existance_result_for_year == True:
                self.create_studio_holidays_for_year(year=str(year), studio_obj=studio_obj)
            
            # get holidays from DB
            holiday_filter_result = self.get_holidays_for_year(year=year,studio_obj=studio_obj)
            
            # prepare holiday reponse data
            if holiday_filter_result[0] == True:
                prepare_holiday_data(holiday_qs=holiday_filter_result[1])
                result["is_holiday"] = True
            else:
                result["is_holiday"] = False
                    
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)

    
    def check_holidays_from_list(self, request, *args, **kwargs):
        """ *** Parent Method for checking holidays from list *** """
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
            
            date_list = request.data.get("date_list", [])
            
            result = {
                "date_list": date_list,
                "studio": studio,
                "is_holiday": False,
                "total_holidays": 0,
                "holidays": []
            }
            
            def prepare_holiday_data(holiday_qs=None):
                holiday_list = []
                for holiday in holiday_qs:
                    data = {}
                    data["title"] = holiday.title
                    data["comments"] = holiday.comments
                    data["country_code"] = holiday.country_code
                    data["year"] = holiday.year
                    data["date"] = holiday.date
                    holiday_list.append(data)
                result['holidays'] = holiday_list
                result['total_holidays'] = len(holiday_list)
                return result
            
            
            checked_year_list = []
            holiday_objects = []
            
            for date in date_list:
                date_obj = None
                try:
                    date_obj = parser.parse(date)
                except Exception as e:
                    return ResponseWrapper(error_code=400, error_msg=serializer.errors, msg=f"Got invalid date format. Failed to parse date! Exception: {str(e)}", status=400)
                
                year = date_obj.year
                
                formatted_date_str = date_obj.strftime("%Y-%m-%d")
                
                # check if studio holidays exists for year
                holiday_existance_result_for_year = False
                if not year in checked_year_list:
                    holiday_existance_result_for_year = self.check_studio_holidays_exists_for_year(year=year, studio_obj=studio_obj)
                    checked_year_list.append(year)
                else:
                    holiday_existance_result_for_year = True

                # create holidays for year if not exists
                if not holiday_existance_result_for_year == True:
                    self.create_studio_holidays_for_year(year=str(year), studio_obj=studio_obj)
                
                # get holidays from DB
                holiday_filter_result = self.get_single_holiday(date=formatted_date_str, studio_obj=studio_obj)
                
                # prepare holiday reponse data
                if holiday_filter_result[0] == True:
                    holiday_objects.append(holiday_filter_result[1])
                    if not result["is_holiday"] == True:
                        result["is_holiday"] = True
                
            # prepare holiday reponse data
            if result["is_holiday"] == True:
                prepare_holiday_data(holiday_qs=holiday_objects)
                        
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)
