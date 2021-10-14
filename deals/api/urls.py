from django.urls import path
from rest_framework.routers import DefaultRouter
from .coupon_views import CouponManagerViewSet
from .point_setting_views import PointManagerViewSet

router = DefaultRouter()

urlpatterns = [
    # ==============================*** Deal URLS ***==============================
    path("coupon/create", CouponManagerViewSet.as_view({'post': 'create'}, name='create_coupon')),
    path("coupon/retrieve/<slug>", CouponManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_coupon")),
    path("coupon/update/<slug>", CouponManagerViewSet.as_view({"patch": "update"}, name="update_coupon")),
    path("coupon/delete/<slug>", CouponManagerViewSet.as_view({"delete": "destroy"}, name="delete_coupon")),
    path("coupon/list/<studio_slug>", CouponManagerViewSet.as_view({"get": "list"}, name="list_coupon")),

    # ==============================*** Deal Point URLS ***==============================
    path("point/create", PointManagerViewSet.as_view({'post': 'create'}, name='create_point')),
    path("point/retrieve/<slug>", PointManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_point")),
    path("point/update/<slug>", PointManagerViewSet.as_view({"patch": "update"}, name="update_point")),
    path("point/delete/<slug>", PointManagerViewSet.as_view({"delete": "destroy"}, name="delete_point")),
    path("point/list/<studio_slug>", PointManagerViewSet.as_view({"get": "list"}, name="list_point")),

]
