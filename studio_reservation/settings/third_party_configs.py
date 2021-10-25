""" # Project Third Party Configurations # """

# imports
from datetime import timedelta
import environ
import os
from pathlib import Path

""" *** Project Directory Configurations *** """
BASE_DIR = Path(__file__).resolve().parent.parent.parent

""" *** Reading Project Environment *** """
env = environ.Env()
env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

"""
----------------------- * Django CORS Configuration * -----------------------
"""

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     'http://127.0.0.1',
#     'http://localhost',
#     'http://157.245.201.79',
#     'http://192.168.100.247',
#     'http://192.168.0.102',
# ]

# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = ('http://localhost:5000',)
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = ['*']

"""
----------------------- * Rest Framework Configuration * -----------------------
"""
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'EXCEPTION_HANDLER': 'utils.helpers.custom_exception_handler',
    # 'EXCEPTION_HANDLER': 'utils.custom_exception_handler.handle_exception',
}

"""
----------------------- * Rest-Auth Configuration * -----------------------
"""
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.api.serializers.RegisterSerializer',
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.api.serializers.RegisterSerializer',
    'LOGIN_SERIALIZER': 'users.api.serializers.LoginSerializer',
}

"""
----------------------- * Simple JWT Configuration * -----------------------
"""
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=43800),  # 1 Month
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env.str('SECRET_KEY'),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=43800),  # 1 Month
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=30),
}

"""
----------------------- * Django Allauth Configuration * -----------------------
"""
LOGIN_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'  # mandatory, optional, none
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"

"""
----------------------- * Yet Another Swagger Configuration * -----------------------
"""

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'JSON_EDITOR': True,
    # 'USE_SESSION_AUTH': True,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

"""
----------------------- * Django Faker * -----------------------
"""

FAKER_LOCALE = None     # settings.LANGUAGE_CODE is loaded
FAKER_PROVIDERS = None  # faker.DEFAULT_PROVIDERS is loaded (all)


"""
----------------------- * File Configurations * -----------------------
"""
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # Django Default 2.5 MB | 5 MB

FILE_SIZE_LIMIT_IN_BYTES = 1572864 # 1.5 MB
ALLOWED_IMAGE_TYPES = ['.jpg', '.jpeg', '.png']
ALLOWED_DOCUMENT_TYPES = ['.doc', '.docx', '.pdf']
MAX_UPLOAD_SIZE = 2621440 # KB
ALLOWED_FILE_TYPES = ALLOWED_IMAGE_TYPES + ALLOWED_DOCUMENT_TYPES
