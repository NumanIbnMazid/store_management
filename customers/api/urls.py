from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import(
    AccountManagerViewSet
)


router = DefaultRouter()

urlpatterns = [
    # ==============================*** CUSTOMER URLS ***==============================
    path("create", AccountManagerViewSet.as_view({"post": "create"}, name="create_customer")),
    path("retrieve/<slug>", AccountManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_customer")),
    path("update/<slug>", AccountManagerViewSet.as_view({"patch": "update"}, name="update_customer")),
    # path("delete/<slug>/", AccountManagerViewSet.as_view({"delete": "destroy"}, name="delete_customer")),
]