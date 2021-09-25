from django.urls import path
from rest_framework.routers import DefaultRouter
from .category_views import CategoryManagerViewSet
from .option_views import OptionManagerViewSet
from .product_views import ProductManagerViewSet

router = DefaultRouter()

urlpatterns = [
    # ==============================*** Category URLS ***==============================
    path("category/create/", CategoryManagerViewSet.as_view({'post': 'create'}, name='create_category')),
    path("category/retrieve/<slug>/", CategoryManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_category")),
    path("category/update/<slug>/", CategoryManagerViewSet.as_view({"patch": "update"}, name="update_category")),
    path("category/delete/<slug>/", CategoryManagerViewSet.as_view({"delete": "destroy"}, name="delete_category")),

    # ==============================*** Option URLS ***==============================
    path("option/create/", OptionManagerViewSet.as_view({'post': 'create'}, name='create_option')),
    path("option/retrieve/<slug>/", OptionManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_option")),
    path("option/update/<slug>/", OptionManagerViewSet.as_view({"patch": "update"}, name="update_option")),
    path("option/delete/<slug>/", OptionManagerViewSet.as_view({"delete": "destroy"}, name="delete_option")),

    # ==============================*** Product URLS ***==============================
    path("product/create/", ProductManagerViewSet.as_view({'post': 'create'}, name='create_product')),
    path("product/retrieve/<slug>/", ProductManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_product")),
    path("product/update/<slug>/", ProductManagerViewSet.as_view({"patch": "update"}, name="update_product")),
    path("product/delete/<slug>/", ProductManagerViewSet.as_view({"delete": "destroy"}, name="delete_product")),
]


