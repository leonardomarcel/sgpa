import os
from e_ouv_alagoas.settings.settings import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'prd_eouv',
        'USER': 'adm_eouv',
        'PASSWORD': 'bruB7LR=n=',
        'HOST': '10.1.16.173',
        'PORT': '5432',
    },
    
    'e_sic': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hml_esic',
        'USER': 'adm_esic',
        'PASSWORD': 'pewreSt!kE8a',
        'HOST': '10.1.16.175',
        'PORT': '5432',
    }
}