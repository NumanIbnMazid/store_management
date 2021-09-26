""" # Development Environment Configurations # """
# import common configurations
from studio_reservation.settings.common import *

""" *** Application Allowed Hosts *** """
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

""" *** Database Configuration *** """
# if env.str('DATABASE_URL', default=''):
#     DATABASES = {
#         'default': env.db(),
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }


# ======= ELEPHANT POSTGRESQL =======
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env.str('ELEPHANT_DB_NAME'),
        'USER': env.str('ELEPHANT_DB_USER'),
        'PASSWORD': env.str('ELEPHANT_DB_PASSWORD'),
        'HOST': env.str('ELEPHANT_DB_HOST'),
        'PORT': env.int('ELEPHANT_DB_PORT'),
        # 'OPTIONS': {
        #     'charset': 'utf8mb4',
        #     'autocommit': True,
        #     'use_unicode': True,
        #     'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8mb4,collation_connection=utf8mb4_unicode_ci',
        #     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        # },
    }
}
