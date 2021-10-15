from django.urls import path
from rest_framework.routers import DefaultRouter
from .coupon_views import CouponManagerViewSet
from .point_setting_views import PointSettingManagerViewSet

router = DefaultRouter()

urlpatterns = [
    # ==============================*** Deal URLS ***==============================
    path("coupon/create", CouponManagerViewSet.as_view({'post': 'create'}, name='create_coupon')),
    path("coupon/retrieve/<slug>", CouponManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_coupon")),
    path("coupon/update/<slug>", CouponManagerViewSet.as_view({"patch": "update"}, name="update_coupon")),
    path("coupon/delete/<slug>", CouponManagerViewSet.as_view({"delete": "destroy"}, name="delete_coupon")),
    path("coupon/list/<studio_slug>", CouponManagerViewSet.as_view({"get": "list"}, name="list_coupon")),

    # ==============================*** PointSetting URLS ***==============================
    path("point-setting/create", PointSettingManagerViewSet.as_view({'post': 'create'}, name='create_point_setting')),
    path("point-setting/retrieve/<slug>", PointSettingManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_point_setting")),
    path("point-setting/update/<slug>", PointSettingManagerViewSet.as_view({"patch": "update"}, name="update_point_setting")),
    path("point-setting/delete/<slug>", PointSettingManagerViewSet.as_view({"delete": "destroy"}, name="delete_point_setting")),
    path("point-setting/list/<studio_slug>", PointSettingManagerViewSet.as_view({"get": "list"}, name="list_point_setting")),

]
