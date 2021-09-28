""" # Production Environment Configurations # """
# import common configurations
from studio_reservation.settings.common import *
import django_heroku
import dj_database_url

""" *** Application Allowed Hosts *** """
ALLOWED_HOSTS = ["studio-reservation.herokuapp.com"]

""" *** Database Configuration *** """

# ======= HEROKU POSTGRESQL =======
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('HEROKU_DB_NAME'),
        'USER': env.str('HEROKU_DB_USER'),
        'PASSWORD': env.str('HEROKU_DB_PASSWORD'),
        'HOST': env.str('HEROKU_DB_HOST'),
        'PORT': env.int('HEROKU_DB_PORT'),
    }
}

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)


# Activate Django-Heroku.
django_heroku.settings(locals())
