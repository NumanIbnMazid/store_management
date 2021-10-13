from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StoreManagerViewSet, CustomBusinessDayManagerViewSet
from .business_day_views import BusinessDayManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Store URLS ***==============================
    path("create", StoreManagerViewSet.as_view({'post': 'create'}, name='create_store')),
    path("retrieve/<slug>", StoreManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_store")),
    path("update/<slug>", StoreManagerViewSet.as_view({"patch": "update"}, name="update_store")),
    path("delete/<slug>", StoreManagerViewSet.as_view({"delete": "destroy"}, name="delete_store")),
    path("list/<studio_slug>", StoreManagerViewSet.as_view({"get": "list"}, name="list_store")),
    
    # ==============================*** CustomClosedDay URLS ***==============================
    path("custom-business-day/create", CustomBusinessDayManagerViewSet.as_view({'post': 'create'}, name='create_custom_business_day')),
    path("custom-business-day/retrieve/<slug>", CustomBusinessDayManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_custom_business_day")),
    path("custom-business-day/update/<slug>", CustomBusinessDayManagerViewSet.as_view({"patch": "update"}, name="update_custom_business_day")),
    path("custom-business-day/delete/<slug>", CustomBusinessDayManagerViewSet.as_view({"delete": "destroy"}, name="delete_custom_business_day")),
    
    # ==============================*** Store BusinessDay URLS ***==============================
    path("get-single-business-day-status", BusinessDayManagerViewSet.as_view(
            {"post": "check_single_business_day_status"}, name="check_single_business_day_status"
        )
    ),
    path("get-business-days-by-year", BusinessDayManagerViewSet.as_view(
            {"post": "get_business_days_by_year"}, name="get_business_days_by_year"
        )
    ),
]
