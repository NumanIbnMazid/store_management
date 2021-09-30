from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudioCalendarManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Studio Calendar URLS ***==============================
    path("get-single-holiday-status/", StudioCalendarManagerViewSet.as_view({"post": "check_single_holiday"}, name="check_single_holiday")),
    path("get-holidays-by-range/", StudioCalendarManagerViewSet.as_view({"post": "check_holidays_between_range"}, name="check_holidays_between_range")),
    path("get-holidays-by-year/", StudioCalendarManagerViewSet.as_view({"post": "check_holidays_for_year"}, name="check_holidays_for_year")),
    path("get-holidays-by-list/", StudioCalendarManagerViewSet.as_view({"post": "check_holidays_from_list"}, name="check_holidays_from_list")),
]
