from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StoreManagerViewSet, CustomBusinessDayManagerViewSet, StoreModeratorManagerViewSet
from .business_day_views import BusinessDayManagerViewSet
from .business_hour_views import StoreBusinessHourManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Store URLS ***==============================
    path("create", StoreManagerViewSet.as_view({'post': 'create'}, name='create_store')),
    path("retrieve/<slug>", StoreManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_store")),
    path("update/<slug>", StoreManagerViewSet.as_view({"patch": "update"}, name="update_store")),
    path("delete/<slug>", StoreManagerViewSet.as_view({"delete": "destroy"}, name="delete_store")),
    path("list/<studio_slug>", StoreManagerViewSet.as_view({"get": "list"}, name="list_store")),
    path("dynamic-list", StoreManagerViewSet.as_view({"get": "dynamic_list"}, name="store_dynamic_list")),
    path("list-with-short-info/<studio_slug>", StoreManagerViewSet.as_view({"get": "list_with_short_info"}, name="store_list_with_short_info")),
    path("get-store-for-business-hour-from-studio/<studio_slug>", StoreManagerViewSet.as_view(
        {"get": "get_store_for_business_hour_from_studio"}, name="get_store_for_business_hour_from_studio")),
    
     # ==============================*** StudioModerator URLS ***==============================
    # path("moderator/create/admin", StoreModeratorManagerViewSet.as_view({'post': 'create_admin'}, name='create_studio_admin')),
    path("moderator/create/staff", StoreModeratorManagerViewSet.as_view({'post': 'create_staff'}, name='create_store_staff')),
    path("moderator/retrieve/<slug>", StoreModeratorManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_store_moderator")),
    path("moderator/update/<slug>", StoreModeratorManagerViewSet.as_view({"patch": "update"}, name="update_store_moderator")),
    # path("moderator/delete/admin/<slug>", StoreModeratorManagerViewSet.as_view({"delete": "destroy_admin"}, name="delete_store_admin")),
    path("moderator/delete/staff/<slug>", StoreModeratorManagerViewSet.as_view({"delete": "destroy_staff"}, name="delete_store_staff")),
    path("moderator/list/staff/<store_slug>", StoreModeratorManagerViewSet.as_view({"get": "list"}, name="list_store_staff")),
    path("moderator/dynamic-list", StoreModeratorManagerViewSet.as_view({"get": "dynamic_list"}, name="store_staff_dynamic_list")),
    
    # ==============================*** CustomClosedDay URLS ***==============================
    path("custom-business-day/create", CustomBusinessDayManagerViewSet.as_view({'post': 'create'}, name='create_custom_business_day')),
    path("custom-business-day/retrieve/<slug>", CustomBusinessDayManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_custom_business_day")),
    path("custom-business-day/update/<slug>", CustomBusinessDayManagerViewSet.as_view({"patch": "update"}, name="update_custom_business_day")),
    path("custom-business-day/delete/<slug>", CustomBusinessDayManagerViewSet.as_view({"delete": "destroy"}, name="delete_custom_business_day")),
    path("custom-business-day/dynamic-list", CustomBusinessDayManagerViewSet.as_view({"get": "dynamic_list"}, name="custom_business_day_dynamic_list")),
    
    # ==============================*** Store BusinessDay URLS ***==============================
    path("get-single-business-day-status", BusinessDayManagerViewSet.as_view(
            {"post": "check_single_business_day_status"}, name="check_single_business_day_status"
        )
    ),
    path("get-business-days-by-year", BusinessDayManagerViewSet.as_view(
            {"post": "get_business_days_by_year"}, name="get_business_days_by_year"
        )
    ),
    path("get-business-days-by-range", BusinessDayManagerViewSet.as_view(
            {"post": "get_business_days_by_range"}, name="get_business_days_by_range"
        )
    ),

    # ==============================*** Store Business Hours URLS ***==============================
    path("store-business-hour/create", StoreBusinessHourManagerViewSet.as_view(
        {'post': 'create'}, name='create_store_business_hour')),
    path("store-business-hour/retrieve/<slug>", StoreBusinessHourManagerViewSet.as_view(
        {"get": "retrieve"}, name="retrieve_store_business_hour")),
    path("store-business-hour/update/<slug>", StoreBusinessHourManagerViewSet.as_view(
        {"patch": "update"}, name="update_store_business_hour")),
    path("store-business-hour/delete/<slug>", StoreBusinessHourManagerViewSet.as_view(
        {"delete": "destroy"}, name="delete_store_business_hour")),
    path("store-business-hour/dynamic-list", StoreBusinessHourManagerViewSet.as_view(
        {"get": "dynamic_list"}, name="custom_store_business_hour")),
]
