from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SpaceManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Space URLS ***==============================
    path("create", SpaceManagerViewSet.as_view({'post': 'create'}, name='create_space')),
    path("retrieve/<slug>", SpaceManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_space")),
    path("update/<slug>", SpaceManagerViewSet.as_view({"patch": "update"}, name="update_space")),
    path("delete/<slug>", SpaceManagerViewSet.as_view({"delete": "destroy"}, name="delete_space")),
    path("list/<store_slug>", SpaceManagerViewSet.as_view({"get": "list"}, name="list_space")),
    path("list-with-short-info/<store_slug>", SpaceManagerViewSet.as_view({"get": "list_with_short_info"}, name="space_list_with_short_info")),
    path("dynamic-list", SpaceManagerViewSet.as_view({"get": "dynamic_list"}, name="space_dynamic_list")),
]
