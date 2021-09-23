""" # Production Environment Configurations # """
# import common configurations
from studio_reservation.settings.common import *

""" *** Application Allowed Hosts *** """
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

""" *** Database Configuration *** """
if env.str('DATABASE_URL', default=''):
    DATABASES = {
        'default': env.db(),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
