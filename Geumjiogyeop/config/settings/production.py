from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*', '175.45.194.93']

DJANGO_APPS += [
    'corsheaders',
]
PROJECT_APPS += [

]
THIRD_PARTY_APPS += [

]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

APPEND_SLASH = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = False  # 모든 도메인을 허용할지 설정
CORS_ALLOWED_ORIGINS = [       # 접근을 허용할 도메인 목록
    'https://kr.object.ncloudstorage.com/geumjioyeop-bucket/index.html',
]

STATIC_ROOT = BASE_DIR / 'static'