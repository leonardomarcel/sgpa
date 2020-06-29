import os
from e_ouv_alagoas.settings.settings import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'hml_sgpa',
        #'USER': 'adm_sgpa',
        #'PASSWORD': 'KBkjfkTB47ef',
        #'HOST': '10.1.16.175',
        'NAME': 'sgpa2',
        'USER': 'postgre',
        'PASSWORD': 'postgre',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    
   
}