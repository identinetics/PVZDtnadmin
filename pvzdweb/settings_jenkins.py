import ldap
import logging.config
import os
from pvzdweb.settings_base import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.append('ldapgvat')
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pvzddb',
        'USER': 'postgres',
        'PASSWORD': 'changeit',  # superuser password for PostgreSQL
        'HOST': 'mypostgreshost',
        'PORT': '5432',
    },
    'admin_db': {  # same instance as above, but using postgres-db to drop/create the default db
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'changeit',  # superuser password for PostgreSQL
        'HOST': 'mypostgreshost',
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
DBADMIN_SHELL = (
    'psql',
    '-U', DATABASES['admin_db']['USER'],
    '-h', DATABASES['admin_db']['HOST'],
    '-p', DATABASES['admin_db']['PORT'],
    '-d', DATABASES['admin_db']['NAME'],
)

logdir = os.environ.get('PVZDLOGDIR', os.getcwd()+'/work')
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
            'filename': os.path.join(logdir, 'pvzdweb.log'),
            'maxBytes': 1024*1024*500, # 500 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(logdir, 'pvzdweb_request.log'),
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
