""" # Production Environment Configurations # """
# import common configurations
from studio_reservation.settings.common import *
import django_heroku
import dj_database_url

""" *** Application Allowed Hosts *** """
ALLOWED_HOSTS = ["studio-reservation.herokuapp.com"]

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
    

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)


# Activate Django-Heroku.
django_heroku.settings(locals())
