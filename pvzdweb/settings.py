import logging
import os
from os.path import join as opj

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'a)$#m^s5*4zv5i&o9p7gn$6iyp7qd&*oev#9b$*30)542@szdg')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

#MENU_WEIGHT = {
#    'GvOrganisation': 20,
#    'GvFederationOrg': 15,
#    'GvUserPortal': 10,
#    'GvFederation': 5
#}

INSTALLED_APPS = [
    # 'admin_menu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fedop',
    'portaladmin',
    #'portaladmin.apps.PortaladminConfig',
    'tnadmin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pvzddb',
        'USER': 'postgres',
        'PASSWORD': 'changeit',  # superuser password for PostgreSQL
        'HOST': 'postgres',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

PORTALADMIN_CHECKOUT_MINUTES = 15

PVZD_SETTINGS = {
    'logfilepep': opj(*'PVZDlib/PVZDpy/tests/testdout/pep.log'.split('/')),
    'loglevelpep': logging.DEBUG,
    'loglevelweb': logging.DEBUG,
    'pepoutdir': opj(*'PVZDlib/PVZDpy/tests/testout/pepout'.split('/')),
    'poldirhtml': opj(*'PVZDlib/PVZDpy/tests/testout/poldir/poldir.html'.split('/')),
    'poldirjson': opj(*'PVZDlib/PVZDpy/tests/testout/poldir/poldir.json'.split('/')),
    'policydir': opj(BASE_DIR, *'PVZDlib/PVZDpy/tests/testdata/saml/poldir1.json'.split('/')),
    'policyjournal': opj(*'PVZDlib/PVZDpy/tests/testdata/aodsfilehandler/pol_journal_sig_rh.xml'.split('/')),
    'regauthority': 'Bundeskanzleramt',
    'shibacl': opj(*'PVZDlib/PVZDpy/tests/testdout/poldir/shibacl.xml'.split('/')),
    'superuser': True,  # allow signer in trustedcerts to skip authorization check
    'trustedcerts': opj(*'PVZDlib/PVZDpy/tests/testdata/aodsfilehandler/trustedcerts_rh.json'.split('/')),
}
