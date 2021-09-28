from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudioCalendarManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Studio Calendar URLS ***==============================
    path("get-single-holiday-status/", StudioCalendarManagerViewSet.as_view({"post": "check_single_holiday"}, name="check_single_holiday")),
]
