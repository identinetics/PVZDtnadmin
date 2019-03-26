import ldap
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

# === configure here for deployment
# PVZDweb (Fedop, Portaladmin) as seen by the browser:
PVZD_ORIGIN = 'http://localhost:8080'
# Signature Proxy (recommended to be on same host & port -> nginx reverse proxy dispatches on rootpath)
SIGPROXY_ORIGIN = 'http://localhost:8080'

SIGPROXYAPI_ROOTURL = PVZD_ORIGIN  + '/' + SIGPROXYAPI_ROOTPATH
SIGPROXY_BASEURL = SIGPROXY_ORIGIN + '/' 'SigProxy/loadsigproxyclient'
