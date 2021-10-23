from django.urls import path
from rest_framework.routers import DefaultRouter
from .coupon_views import CouponManagerViewSet
from .point_setting_views import PointSettingManagerViewSet
from .earlybird_discount_views import EarlyBirdDiscountManagerViewSet
from .periodical_discount_views import PeriodicalDiscountManagerViewSet

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

    # ==============================*** Early Bird Discount URLS ***==============================
    path("earlybird-discount/create", EarlyBirdDiscountManagerViewSet.as_view(
        {'post': 'create'}, name='create_earlybird_discount')),
    path("earlybird-discount/retrieve/<slug>", EarlyBirdDiscountManagerViewSet.as_view(
        {"get": "retrieve"}, name="retrieve_earlybird_discount")),
    path("earlybird-discount/update/<slug>", EarlyBirdDiscountManagerViewSet.as_view(
        {"patch": "update"}, name="update_earlybird_discount")),
    path("earlybird-discount/delete/<slug>", EarlyBirdDiscountManagerViewSet.as_view(
        {"delete": "destroy"}, name="delete_earlybird_discount")),
    path("earlybird-discount/list/<studio_slug>",
         PointSettingManagerViewSet.as_view({"get": "list"}, name="list_earlybird_discount")),

    # ==============================*** Periodical Discount URLS ***==============================
    path("periodical-discount/create", PeriodicalDiscountManagerViewSet.as_view(
        {'post': 'create'}, name='create_periodical-discount')),
    path("periodical-discount/retrieve/<slug>", PeriodicalDiscountManagerViewSet.as_view(
        {"get": "retrieve"}, name="retrieve_periodical-discount")),
    path("periodical-discount/update/<slug>", PeriodicalDiscountManagerViewSet.as_view(
        {"patch": "update"}, name="update_periodical-discount")),
    path("periodical-discount/delete/<slug>", PeriodicalDiscountManagerViewSet.as_view(
        {"delete": "destroy"}, name="delete_periodical-discount")),
    path("periodical-discount/list/<studio_slug>",
         PointSettingManagerViewSet.as_view({"get": "list"}, name="list_periodical-discount")),

]
