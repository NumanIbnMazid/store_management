from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SpaceManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Space URLS ***==============================
    path("create/", SpaceManagerViewSet.as_view({'post': 'create'}, name='create_space')),
    path("retrieve/<slug>/", SpaceManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_space")),
    path("update/<slug>/", SpaceManagerViewSet.as_view({"patch": "update"}, name="update_space")),
    path("delete/<slug>/", SpaceManagerViewSet.as_view({"delete": "destroy"}, name="delete_space")),
]
