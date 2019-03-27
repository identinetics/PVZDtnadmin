import ldap
import logging.config
import os
from pvzdweb.settings_base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pvzddb',
        'USER': 'postgres',
        'PASSWORD': 'changeit',  # superuser password for PostgreSQL
        'HOST': 'postgres_ci',
        'PORT': '5432',
    },
    'ldap': {
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': 'ldap://openldap_pv:12389',
        'USER': 'cn=admin,dc=at',
        'PASSWORD': 'changeit',
        # 'TLS': ,
        'CONNECTION_OPTIONS': {
            ldap.OPT_X_TLS_DEMAND: False,
        }
    },
}
DATABASE_ROUTERS = ['ldapdb.router.Router']

logdir = os.environ.get('PVZDLOGDIR', 'work')
os.makedirs(logdir, exist_ok=True)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(logdir, '/pvzdweb.log'),
            'maxBytes': 1024*1024*500, # 500 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(logdir, '/pvzdweb_request.log'),
            'maxBytes': 1024*1024*500, # 500 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
LOGGING_CONFIG = None
logging.config.dictConfig(LOGGING)



# === configure here for deployment
# PVZDweb (Fedop, Portaladmin) as seen by the browser:
PVZD_ORIGIN = 'http://localhost:8080'
# Signature Proxy (recommended to be on same host & port -> nginx reverse proxy dispatches on rootpath)
SIGPROXY_ORIGIN = 'http://localhost:8080'

SIGPROXYAPI_ROOTURL = PVZD_ORIGIN  + '/' + SIGPROXYAPI_ROOTPATH
SIGPROXY_BASEURL = SIGPROXY_ORIGIN + '/' 'SigProxy/loadsigproxyclient'
