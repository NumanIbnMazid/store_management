from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** User URLS ***==============================
    path("retrieve/<slug>", UserManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_user")),
    path("update/<slug>", UserManagerViewSet.as_view({"patch": "update"}, name="update_user")),
    # path("delete/<slug>", UserManagerViewSet.as_view({"delete": "destroy"}, name="delete_user")),
    path("list", UserManagerViewSet.as_view({"get": "list"}, name="user_list")),
]
