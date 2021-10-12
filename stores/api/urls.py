from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StoreManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Store URLS ***==============================
    path("create", StoreManagerViewSet.as_view({'post': 'create'}, name='create_store')),
    path("retrieve/<slug>", StoreManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_store")),
    path("update/<slug>", StoreManagerViewSet.as_view({"patch": "update"}, name="update_store")),
    path("delete/<slug>", StoreManagerViewSet.as_view({"delete": "destroy"}, name="delete_store")),
    path("list/<studio_slug>", StoreManagerViewSet.as_view({"get": "list"}, name="list_store")),
]
