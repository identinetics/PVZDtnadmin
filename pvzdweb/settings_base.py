import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.environ.get('DJANGO_DEBUG', False):
    DEBUG = True
else:
    DEBUG = False
if not DEBUG and 'DJANGO_SECRET_KEY' not in os.environ:
    raise Exception('environment variable DJANGO_SECRET_KEY not set')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'secretwithsomemildformofrandomness@s564zdg')

INSTALLED_APPS = [
    # 'bootstrap4',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fedop',
    'portaladmin',
    'rest_framework',
    'tnadmin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'common.custom_header_middleware.CustomHeaderMiddleware',
    'identity.external.PersistentRemoteUserMiddlewareVar',
    'identity.external.RemoteUserAttrMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pvzdweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pvzdweb.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/
LANGUAGE_CODE = 'de'
# LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/Vienna'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}


SIGPROXYAPI_ROOTPATH = 'sigproxyapi'  # do NOT to have a leading /
# === configure SigProxy API paths
SIGPROXYAPI_FEDOP_GETSTARTURL = SIGPROXYAPI_ROOTPATH + '/fedop/getstarturl/'
SIGPROXYAPI_FEDOP_GETUNSIGNEDXML = SIGPROXYAPI_ROOTPATH + '/fedop/getunsignedxml/'
SIGPROXYAPI_FEDOP_POSTSIGNEDXML = SIGPROXYAPI_ROOTPATH + '/fedop/postsignedxml/'
SIGPROXYAPI_FEDOP_STARTSIGNING =  SIGPROXYAPI_ROOTPATH + '/startsigning/'

SIGPROXYAPI_PADMIN_GETSTARTURL = SIGPROXYAPI_ROOTPATH + '/padmin/getstarturl/'
SIGPROXYAPI_PADMIN_GETUNSIGNEDXML = SIGPROXYAPI_ROOTPATH + '/padmin/getunsignedxml/'
SIGPROXYAPI_PADMIN_POSTSIGNEDXML = SIGPROXYAPI_ROOTPATH + '/padmin/postsignedxml/'
SIGPROXYAPI_PADMIN_STARTSIGNING =  SIGPROXYAPI_ROOTPATH + '/startsigning/'
