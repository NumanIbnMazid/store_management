from django.urls import path
from rest_framework.routers import DefaultRouter
from .option_category_views import OptionCategoryManagerViewSet
from .option_views import OptionManagerViewSet
from .plan_views import PlanManagerViewSet

router = DefaultRouter()

urlpatterns = [
    # ==============================*** Option Category URLS ***==============================
    path("option-category/create", OptionCategoryManagerViewSet.as_view({'post': 'create'}, name='create_option_category')),
    path("option-category/retrieve/<slug>", OptionCategoryManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_option_category")),
    path("option-category/update/<slug>", OptionCategoryManagerViewSet.as_view({"patch": "update"}, name="update_option_category")),
    path("option-category/delete/<slug>", OptionCategoryManagerViewSet.as_view({"delete": "destroy"}, name="delete_option_category")),
    path("option-category/list/<studio_slug>", OptionCategoryManagerViewSet.as_view({"get": "list"}, name="list_option_category")),
    path("option-category/dynamic-list", OptionCategoryManagerViewSet.as_view({"get": "dynamic_list"}, name="option_category_dynamic_list")),
    # ==============================*** Option URLS ***==============================
    path("option/create", OptionManagerViewSet.as_view({'post': 'create'}, name='create_option')),
    path("option/retrieve/<slug>", OptionManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_option")),
    path("option/update/<slug>", OptionManagerViewSet.as_view({"patch": "update"}, name="update_option")),
    path("option/delete/<slug>", OptionManagerViewSet.as_view({"delete": "destroy"}, name="delete_option")),
    path("option/list/<option_category_slug>", OptionManagerViewSet.as_view({"get": "list"}, name="list_option")),
    path("option/dynamic-list", OptionManagerViewSet.as_view({"get": "dynamic_list"}, name="option_dynamic_list")),

    # ==============================*** Plan URLS ***==============================
    path("create", PlanManagerViewSet.as_view({'post': 'create'}, name='create_plan')),
    path("retrieve/<slug>", PlanManagerViewSet.as_view({"get": "retrieve"}, name="retrieve_plan")),
    path("update/<slug>", PlanManagerViewSet.as_view({"patch": "update"}, name="update_plan")),
    path("delete/<slug>", PlanManagerViewSet.as_view({"delete": "destroy"}, name="delete_plan")),
    path("list/<space_slug>", PlanManagerViewSet.as_view({"get": "list"}, name="list_plan")),
]


