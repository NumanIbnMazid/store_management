from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudioViewSet
from .vat_tax_views import VatTaxManagerViewSet
from .currency_views import CurrencyManagerViewSet


router = DefaultRouter()

urlpatterns = [
    # ==============================*** Studio URLS ***==============================
    path("create", StudioViewSet.as_view({'post': 'create'}, name='create_studio')),
    path("retrieve/<slug>", StudioViewSet.as_view({"get": "retrieve"}, name="retrieve_studio")),
    path("update/<slug>", StudioViewSet.as_view({"patch": "update"}, name="update_studio")),
    path("delete/<slug>", StudioViewSet.as_view({"delete": "destroy"}, name="delete_studio")),
    path("list", StudioViewSet.as_view({"get": "list"}, name="list_studio")),

    # ==============================*** Vat Tax URLS ***==============================
    path("vattax/create", VatTaxManagerViewSet.as_view({'post': 'create'}, name='create_vat_tax')),
    path("vattax/retrieve/<slug>", VatTaxManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_vat_tax")),
    path("vattax/update/<slug>", VatTaxManagerViewSet.as_view({"patch": "update"}, name="update_vat_tax")),
    path("vattax/delete/<slug>", VatTaxManagerViewSet.as_view({"delete": "destroy"}, name="delete_vat_tax")),
    path("vattax", VatTaxManagerViewSet.as_view({"post": "studio_vat_tax"}, name="studio_vat_tax")),
    path("vattax/list/<studio_slug>", VatTaxManagerViewSet.as_view({"get": "list"}, name="list_studio_vat_tax")),

    # ==============================*** Currency URLS ***==============================
    path("currency/create", CurrencyManagerViewSet.as_view({'post': 'create'}, name='create_currency')),
    path("currency/retrieve/<slug>", CurrencyManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_currency")),
    path("currency/update/<slug>", CurrencyManagerViewSet.as_view({"patch": "update"}, name="update_currency")),
    path("currency/delete/<slug>", CurrencyManagerViewSet.as_view({"delete": "destroy"}, name="delete_currency")),
    path("currency/list/<studio_slug>", CurrencyManagerViewSet.as_view({"get": "list"}, name="list_currency")),
    path("currency/dynamic-list", CurrencyManagerViewSet.as_view({"get": "dynamic_list"}, name="currency_dynamic_list")),
]
