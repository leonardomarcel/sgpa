import os
from sgpa.settings.settings import *

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
        'USER': 'postgres',
        'PASSWORD': 'postgre',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
'''
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'hml_eouv',
    'USER': 'adm_eouv',
    'PASSWORD': 'C?emu3ruswe?',
    'HOST': '10.1.16.175',
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
'''
