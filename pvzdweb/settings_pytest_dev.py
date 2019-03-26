import os
from pvzdweb.settings_dev import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# test ldap:
# ldapsearch -h devl11 -p 8389 -D cn=admin,dc=at -x -w changeit -L 'uid=*'

DATABASES = {
    # sqllite stopped to work properly (created a foreign key that referenced a parent table with suffix _old)
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': ':memory:',
    #},
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pvzddb_nofsync',
        'USER': 'postgres',
        'PASSWORD': 'changeit',  # superuser password for PostgreSQL
        'HOST': 'devl11',
        'PORT': '15432',
    },
    'ldap': {
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': 'ldap://devl11:8389',
        'USER': 'cn=admin,dc=at',
        'PASSWORD': 'changeit',
        # 'TLS': ,
        'CONNECTION_OPTIONS': {
            ldap.OPT_X_TLS_DEMAND: False,
        }
    },
}

# os.environ.setdefault('SQLLITE', 'True')   # signal tnadmin migration not to add postgres-specific constraints
