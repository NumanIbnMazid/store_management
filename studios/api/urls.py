from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudioViewSet, StudioModeratorManagerViewSet
from .vat_tax_views import VatTaxManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Studio URLS ***==============================
    path("create", StudioViewSet.as_view({'post': 'create'}, name='create_studio')),
    path("retrieve/<slug>", StudioViewSet.as_view({"get": "retrieve"}, name="retrieve_studio")),
    path("update/<slug>", StudioViewSet.as_view({"patch": "update"}, name="update_studio")),
    path("delete/<slug>", StudioViewSet.as_view({"delete": "destroy"}, name="delete_studio")),
    # ==============================*** StudioModerator URLS ***==============================
    # path("moderator/create/admin", StudioModeratorManagerViewSet.as_view({'post': 'create_admin'}, name='create_studio_admin')),
    path("moderator/create/staff", StudioModeratorManagerViewSet.as_view({'post': 'create_staff'}, name='create_studio_staff')),
    path("moderator/retrieve/<slug>", StudioModeratorManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_studio_moderator")),
    path("moderator/update/<slug>", StudioModeratorManagerViewSet.as_view({"patch": "update"}, name="update_studio_moderator")),
    # path("moderator/delete/admin/<slug>", StudioModeratorManagerViewSet.as_view({"delete": "destroy_admin"}, name="delete_studio_admin")),
    path("moderator/delete/staff/<slug>", StudioModeratorManagerViewSet.as_view({"delete": "destroy_staff"}, name="delete_studio_staff")),

     # ==============================*** Vat Tax URLS ***==============================
    path("vattax/create", VatTaxManagerViewSet.as_view({'post': 'create'}, name='create_vat_tax')),
    path("vattax/retrieve/<slug>", VatTaxManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_vat_tax")),
    path("vattax/update/<slug>", VatTaxManagerViewSet.as_view({"patch": "update"}, name="update_vat_tax")),
    path("vattax/delete/<slug>", VatTaxManagerViewSet.as_view({"delete": "destroy"}, name="delete_vat_tax")),
    path("vattax", VatTaxManagerViewSet.as_view({"post": "studio_vat_tax"}, name="studio_vat_tax")),
]
