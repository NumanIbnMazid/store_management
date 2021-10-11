from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CouponManagerViewSet

router = DefaultRouter()

urlpatterns = [
    # ==============================*** Deal URLS ***==============================
    path("coupon/create", CouponManagerViewSet.as_view({'post': 'create'}, name='create_coupon')),
    path("coupon/retrieve/<slug>", CouponManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_coupon")),
    path("coupon/update/<slug>", CouponManagerViewSet.as_view({"patch": "update"}, name="update_coupon")),
    path("coupon/delete/<slug>", CouponManagerViewSet.as_view({"delete": "destroy"}, name="delete_coupon")),

]
