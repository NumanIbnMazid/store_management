from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudioCalendarManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Studio Calendar URLS ***==============================
    path("get-single-holiday-status/", StudioCalendarManagerViewSet.as_view({"post": "check_single_holiday"}, name="check_single_holiday")),
    path("get-holiday-from-range/", StudioCalendarManagerViewSet.as_view({"post": "check_holiday_between_range"}, name="check_holiday_between_range")),
    path("get-all-holidays/", StudioCalendarManagerViewSet.as_view({"post": "get_all_holidays"}, name="get_all_holidays")),
]
