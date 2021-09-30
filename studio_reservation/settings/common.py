""" # Project Common Settings # """
from pathlib import Path
import os
import environ

""" *** Project Directory Configurations *** """
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BASE_APP_DIR = Path(__file__).resolve().parent.parent

""" *** Reading Project Environment *** """
env = environ.Env()
env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

""" *** Application Secret Key *** """
SECRET_KEY = env.str('SECRET_KEY')

""" *** DEBUG Configuration *** """
if env.bool('IS_PRODUCTION', default='') == True:
    DEBUG = False
elif env.bool('IS_PRODUCTION', default='') == False and env.bool('IS_STAGING', default='') == True:
    DEBUG = False
else:
    DEBUG = True


""" *** Application Definitions *** """
THIRD_PARTY_APPS = [
    # Django Rest Framework
    "rest_framework",
    "rest_framework.authtoken",
    # Rest Framework JWT
    "rest_framework_simplejwt",
    # Django-Rest-Auth
    "rest_auth",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_auth.registration",
    # Django Filter
    "django_filters",
    # Django Yet Another Swagger
    "drf_yasg",
    # Django Rest Framework Tracking
    "rest_framework_tracking",
]

LOCAL_APPS = [
    "users",
    "customers",
    "staffs",
    "studios",
    "stores",
    "spaces",
    "plans",
    "studio_calendar",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
] + THIRD_PARTY_APPS + LOCAL_APPS


""" *** Authentication Definitions *** """
AUTH_USER_MODEL = 'users.User'

""" *** Middlewares Definitions *** """
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

""" *** Template Definitions *** """
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_APP_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

""" *** Authentication Password Validators *** """
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

""" *** Localization Configuration *** """
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" *** Static & Media Files Configurations *** """
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_APP_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, os.path.join('static_cdn', 'static_root'))
MEDIA_ROOT = os.path.join(BASE_DIR, os.path.join('static_cdn', 'media_root'))

""" *** Other Definitions *** """
SITE_ID = 1
ROOT_URLCONF = 'studio_reservation.urls'
WSGI_APPLICATION = 'studio_reservation.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
HOME_URL = "/"
ADMIN_LOGIN_URL = "/admin/login/"
LOGIN_URL = "/rest-auth/login/"

""" *** Third Party Configurations *** """
from studio_reservation.settings.third_party_configs import *
