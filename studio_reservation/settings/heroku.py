""" # Production Environment Configurations # """
# import common configurations
from studio_reservation.settings.common import *
import django_heroku
import dj_database_url

""" *** Application Allowed Hosts *** """
ALLOWED_HOSTS = ["studio-reservation.herokuapp.com"]

""" *** Database Configuration *** """
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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
        # 'OPTIONS': {
        #     'charset': 'utf8mb4',
        #     'autocommit': True,
        #     'use_unicode': True,
        #     'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8mb4,collation_connection=utf8mb4_unicode_ci',
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        # },
    }
}

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

<<<<<<< HEAD
=======

>>>>>>> e402aa9778f86d399884036dd8ec56a6c0f94efd
# Activate Django-Heroku.
django_heroku.settings(locals())
