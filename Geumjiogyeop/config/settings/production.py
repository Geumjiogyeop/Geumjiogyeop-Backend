from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*', '175.45.194.93']

DJANGO_APPS += [

]
PROJECT_APPS += [

]
THIRD_PARTY_APPS += [

]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

APPEND_SLASH = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'static'