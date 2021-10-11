from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import NotificationManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Store URLS ***==============================
    path("create", NotificationManagerViewSet.as_view({'post': 'create'}, name='create_notification')),
    path("retrieve/<slug>", NotificationManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_notification")),
    path("update/<slug>", NotificationManagerViewSet.as_view({"patch": "update"}, name="update_notification")),
    path("delete/<slug>", NotificationManagerViewSet.as_view({"delete": "destroy"}, name="delete_notification")),
    path("get-studio-notification", NotificationManagerViewSet.as_view({"post": "studio_notifications"}, name="studio_notifications")),
]
