# imports
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from utils.decorators import has_staff_permission_required
from .views import HomeView
from users.api.views import CustomAPILoginView
from rest_auth.views import (
    LogoutView, UserDetailsView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from rest_auth.registration.views import RegisterView, VerifyEmailView
from django.views.generic import TemplateView


# Define Rest Framework Router
router = DefaultRouter()

# Swagger Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Studio Reservation System API",
        default_version='v1',
        description="Studio Reservation System API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="numanibnmazid@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

""" Authentication URL Patterns """

AUTHENTICATION_URL_PATTERNS = [
    path("api/register", RegisterView.as_view(), name="rest_register"),
    path("api/verify-email", VerifyEmailView.as_view(), name="rest_verify_email"),
    url(r"^api/account-confirm-email/(?P<key>[-:\w]+)$", TemplateView.as_view(), name="account_confirm_email"),
    path("api/login", CustomAPILoginView.as_view(), name="rest_login"),
    path("api/logout", LogoutView.as_view(), name="rest_logout"),
    # path("api/user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("api/password/change", PasswordChangeView.as_view(), name="rest_password_change"),
    path("api/password/reset", PasswordResetView.as_view(), name="rest_password_reset"),
    path("api/password/reset/confirm", PasswordResetConfirmView.as_view(), name="rest_password_reset_confirm"),
]

""" Third Party URL Patterns """

THIRD_PARTY_URL_PATTERNS = [
    # Django Rest Framework
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Django Rest Auth
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # Django Rest Framework JWT
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # Yet Another Swagger
    url(r'^swagger(?P<format>\.json|\.yaml)$', has_staff_permission_required(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    url(r'^swagger$', has_staff_permission_required(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    url(r'^redoc$', has_staff_permission_required(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
]

""" Internal App URL Patterns """

INTERNAL_APP_URL_PATTERNS = [
    path("customer/", include(("customers.api.urls", "customers"), namespace="customers")),
    path("staff/", include(("staffs.api.urls", "staffs"), namespace="staffs")),
    path("studio/", include(("studios.api.urls", "studios"), namespace="studios")),
    path("store/", include(("stores.api.urls", "stores"), namespace="stores")),
    path("space/", include(("spaces.api.urls", "spaces"), namespace="spaces")),
    path("plan/", include(("plans.api.urls", "plans"), namespace="plans")),
    path("calendar/", include(("studio_calendar.api.urls", "studio_calendar"), namespace="studio_calendar")),
    path("deal/", include(("deals.api.urls", "deals"), namespace="deals")),
    path("notification/", include(("notifications.api.urls", "notifications"), namespace="notifications")),
]

""" URL Patterns - Main """
urlpatterns = [
    # For handling Static Files in Debug False Mode
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path("", HomeView.as_view(), name="home"),
] + THIRD_PARTY_URL_PATTERNS + AUTHENTICATION_URL_PATTERNS + INTERNAL_APP_URL_PATTERNS

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
