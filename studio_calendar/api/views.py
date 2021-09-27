from datetime import date
from studios.models import Studio
import holidays
from .serializers import StudioCalendarSerializer, StudioCalendarUpdateSerializer, SingleHolidayCheckerSerializer
from studio_calendar.models import StudioCalendar
from rest_framework_tracking.mixins import LoggingMixin
from utils import permissions as custom_permissions
from utils.custom_viewset import CustomViewSet
from utils.helpers import ResponseWrapper
from dateutil import parser


# Select country
# jp_holidays = holidays.JP()

# base_holidays = holidays.HolidayBase()

# print('26-01-2019' in base_holidays)

# base_holidays.append('26-01-2019')

# print('26-01-2019' in base_holidays)


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
        if not qs.exists():
            return False, None
        return True, qs
    
    def get_single_holiday(self, date, studio_obj):
        date_obj = parser.parse(date)
        year = date_obj.year
        qs = StudioCalendar.objects.filter(year=year, date=date_obj, studio=studio_obj)
        if qs.exists():
            return True, qs.first()
        return False, None
        
    
    def check_single_holiday(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            studio = int(request.data.get("studio", None))
            studio_qs = Studio.objects.filter(id=studio)
            studio_obj = None
            if studio_qs.exists():
                studio_obj = studio_qs.first()
            else:
                raise Exception(f"Studio {studio} not exists!")
            date = request.data.get("date", "")
            
            date_obj = parser.parse(date)
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
            if holiday_existance_result[0] == True:
                holiday_model_instance = self.get_single_holiday(date=formatted_date_str, studio_obj=studio_obj)
                if holiday_model_instance[0] == True:
                    prepare_holiday_data(holiday_instance=holiday_model_instance[1])
                else:
                    result["is_holiday"] = False
            else:
                self.create_studio_holidays_for_year(year=str(year), studio_obj=studio_obj)
                holiday_model_instance = self.get_single_holiday(date=formatted_date_str, studio_obj=studio_obj)
                if holiday_model_instance[0] == True:
                    prepare_holiday_data(holiday_instance=holiday_model_instance[1])
                else:
                    result["is_holiday"] = False
                    
            return ResponseWrapper(data=result, status=200)
        return ResponseWrapper(error_msg=serializer.errors, error_code=400)
