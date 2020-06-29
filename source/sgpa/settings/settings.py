"""
Django settings for e_ouv_alagoas project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from os.path import abspath, dirname, join, normpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_ROOT = dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&#xk-8zamma_um+-7m1^gj*24)3y2ty@+asjdio7a70o_g*g+q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['localhost', '10.1.15.70', '10.1.15.76', '10.1.15.59', '10.1.15.29', '127.0.0.1', '192.168.0.4']

LOGIN_URL = "/login/"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'formtools',
    'compressor',
    'pagination_bootstrap',
    'bootstrap_pagination', 
    'ckeditor', 
    'auth_local',
    'passagem',
    'relatorio',
    'basico',
    'reversion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
    'reversion.middleware.RevisionMiddleware'
]

ROOT_URLCONF = 'sgpa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = 'sgpa.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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



# User model
#O projeto utiliza o authenticate()
AUTH_USER_MODEL = 'auth_local.UsuarioOrgao'
#AUTH_USER_MODEL = 'auth_local.UsuarioCidadao'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_INPUT_FORMATS = ('%d/%m/%Y', '%y/%m/%d')

#DATE_FORMAT = ('%d/%m/%Y', '%y/%m/%d')

DATETIME_INPUT_FORMATS = ('%d/%m/%Y %H:%M', '%d/%m/%Y %H:%M:%S'
    '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%Y',
    '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M', '%d/%m/%y'
    )



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))
MEDIA_URL = '/media/'
RELATORIO_CSS =   normpath(join(SITE_ROOT, 'static/css/template_relatorio.scss'))
RELATORIO_CSS_2 =   normpath(join(SITE_ROOT, 'static/css/template_relatorio.scss'))

STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATIC_URL = '/static/'
STATIC_ROOT = normpath(join(SITE_ROOT, 'static_root'))

CKEDITOR_BASEPATH = STATIC_URL + "ckeditor/ckeditor"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike']},
            {'name': 'paragraph', 
             'items': ['NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'yourcustomtools', 'items': [
                'Preview',
                'Maximize',
            ]},
            {'name': 'styles', 'items': ['Format', 'Font', 'FontSize']},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'height': 291,
        'width': '100%',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

# Django libsass configs

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

DEFAULT_EMAIL_FROM = 'suportesistemas.itec@itec.al.gov.br'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.expresso.al.gov.br'
SERVER_EMAIL = 'mail.expresso.al.gov.br'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'suportesistemas.itec'
EMAIL_USE_SSL = False
EMAIL_USE_TLS = False
EMAIL_HOST_PASSWORD = '5ZBbaP'

NOME_SGPA = 'SGPA Alagoas'
EMAIL_NOME_SGPA_ALAGOAS = NOME_SGPA + ' - [E-mail de confirmação nova senha]'
EMAIL_TITLE_SOLICITACAO_PASSAGEM = NOME_SGPA + ' - [Solicitação de Passagem Criada]'
EMAIL_TITLE_PASSAGEM_EMITIDA = NOME_SGPA + ' - [Passagem Emitida]'
EMAIL_TITLE_SOLICITACAO_PASSAGEM_APROVADA = NOME_SGPA + ' - [Solicitação de Passagem Aprovada]'
EMAIL_TITLE_SOLICITACAO_PASSAGEM_REPROVADA = NOME_SGPA + ' - [Solicitação de Passagem Reprovada]'
EMAIL_TITLE_PASSAGEM_REMARCADA = NOME_SGPA + ' - [Passagem Remarcada]'
EMAIL_ASSUNTO_REDEFINICAO_SENHA = NOME_SGPA + ' - [Redefinição de senha]'
EMAIL_FOOTER_NOME_ITEC = 'Instituto de Tecnologia em Informática e Informação do Estado de Alagoas - ITEC/AL'
EMAIL_FOOTER_NOME_AMGESP = 'Ageência de Modernização e Gestão de Processos - AMGESP/AL'
EMAIL_NOME_SGPA_ALAGOAS_COMPLETO = 'SGPA - Sistema de Gestão de Passagens Aéreas do Estado de Alagoas' 
EMAIL_URL_LOGO_ITEC = 'http://e-sic.al.gov.br/static/public/imgs/itec-footer.png'
EMAIL_URL_SITE_PRODUCAO = 'http://e-ouv.al.gov.br'
#EMAIL_URL_SITE_HOMOLOGACAO = 'http://homologa.e-ouv.al.gov.br'

GOOGLE_RECAPTCHA_SECRET_KEY = '6LfWfKIUAAAAAAK9ziQ6AxPISU0e-EZ88YtMlHT_'
GOOGLE_RECAPTCHA_SITE_VERIFY = 'https://www.google.com/recaptcha/api/siteverify'

TASK_UPLOAD_FILE_TYPES = ['pdf', 'jpeg','jpg', 'png']
TASK_UPLOAD_FILE_MAX_SIZE = 2621440

#IP_RELATORIO = "http://172.16.34.13:8080/EOuv-Web-Proxy/execreport"
IP_RELATORIO = "http://localhost:8080/EOuvWebProxy/execreport"

IS_HOMOLOGACAO = True