from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import(
    AccountManagerViewSet
)
from .customer_search_views import CustomerSearchManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** CUSTOMER URLS ***==============================
    path("create", AccountManagerViewSet.as_view({"post": "create"}, name="create_customer")),
    path("retrieve/<slug>", AccountManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_customer")),
    path("update/<slug>", AccountManagerViewSet.as_view({"patch": "update"}, name="update_customer")),
    path("list", AccountManagerViewSet.as_view({"get": "list"}, name="list_customer")),
    # path("delete/<slug>/", AccountManagerViewSet.as_view({"delete": "destroy"}, name="delete_customer")),
    path("search", CustomerSearchManagerViewSet.as_view({"post": "check_customer_between_range"}, name="check_customer_between_range")),

]