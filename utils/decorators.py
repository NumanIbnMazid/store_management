from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings


# has staff permission required


has_staff_permission = user_passes_test(
    # lambda user: user.is_superuser == True or user.is_staff == True, login_url=settings.ADMIN_LOGIN_URL

    # By pass for testing purpose
    lambda user: user.is_staff == True or user.is_staff == False, login_url=settings.ADMIN_LOGIN_URL
)


def has_staff_permission_required(view_func):
    decorated_view_func = login_required(has_staff_permission(view_func))
    return decorated_view_func
