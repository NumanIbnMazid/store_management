from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudioCalendarManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Studio Calendar URLS ***==============================
    path("get-single-holiday-status/", StudioCalendarManagerViewSet.as_view({"post": "check_single_holiday"}, name="check_single_holiday")),
    path("get-holidays-by-range/", StudioCalendarManagerViewSet.as_view({"post": "check_holiday_between_range"}, name="check_holiday_between_range")),
    path("get-holidays-by-year/", StudioCalendarManagerViewSet.as_view({"post": "check_holidays_for_year"}, name="check_holidays_for_year")),
    path("get-holidays-by-list/", StudioCalendarManagerViewSet.as_view({"post": "check_holidays_from_list"}, name="check_holidays_from_list")),

    # ==============================*** Studio Calendar URLS Create Update Delete ***==============================
    path("create/", StudioCalendarManagerViewSet.as_view({'post': 'create'}, name='create_studio_calendar')),
    path("retrieve/<slug>/", StudioCalendarManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_studio_calendar")),
    path("update/<slug>/", StudioCalendarManagerViewSet.as_view({"patch": "update"}, name="update_studio_calendar")),
    path("delete/<slug>/", StudioCalendarManagerViewSet.as_view({"delete": "destroy"}, name="delete_studio_calendar")),
]
