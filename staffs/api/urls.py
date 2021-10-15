from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import(
    StaffAccountManagerViewSet
)


router = DefaultRouter()

urlpatterns = [
    # ==============================*** STAFF URLS ***==============================
    path("create", StaffAccountManagerViewSet.as_view({'post': 'create'}, name='create_staff')),
    path("retrieve/<slug>", StaffAccountManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_staff")),
    path("update/<slug>", StaffAccountManagerViewSet.as_view({"patch": "update"}, name="update_staff")),
    path("delete/<slug>", StaffAccountManagerViewSet.as_view({"delete": "destroy"}, name="delete_staff")),
    path("list/<studio_slug>", StaffAccountManagerViewSet.as_view({"get": "list"}, name="list_staff")),

]


