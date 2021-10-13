from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StoreManagerViewSet, CustomClosedDayManagerViewSet
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
    path("custom-closed-day/create", CustomClosedDayManagerViewSet.as_view({'post': 'create'}, name='create_custom_closed_day')),
    path("custom-closed-day/retrieve/<slug>", CustomClosedDayManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_custom_closed_day")),
    path("custom-closed-day/update/<slug>", CustomClosedDayManagerViewSet.as_view({"patch": "update"}, name="update_custom_closed_day")),
    path("custom-closed-day/delete/<slug>", CustomClosedDayManagerViewSet.as_view({"delete": "destroy"}, name="delete_custom_closed_day")),
    
    # ==============================*** Store BusinessDay URLS ***==============================
    path("get-single-business-day-status", BusinessDayManagerViewSet.as_view(
            {"post": "check_single_business_day_status"}, name="check_single_business_day_status"
        )
    ),
]
