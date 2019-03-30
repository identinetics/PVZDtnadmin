from pathlib import Path
from pvzdweb.settings import *

#
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# test ldap:
# ldapsearch -h devl11 -p 8389 -D cn=admin,dc=at -x -w changeit -L 'uid=*'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pvzddb',
        'USER': 'postgres',
        'PASSWORD': 'changeit',  # superuser password for PostgreSQL
        'HOST': 'devl11',
        'PORT': '5432',
    },
    'admin_db': {  # used to drop/create the default db
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'changeit',  # superuser password for PostgreSQL
        'HOST': 'devl11',
        'PORT': '5432',
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
DBADMIN_SHELL = (
    'psql',
    '-U', DATABASES['admin_db']['USER'],
    '-h', DATABASES['admin_db']['HOST'],
    '-p', DATABASES['admin_db']['PORT'],
    '-d', DATABASES['admin_db']['NAME'],
)


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'database', 'db.sqlite3'),
#     }
# }

INSTALLED_APPS=sorted(list(set(INSTALLED_APPS + ['ldapgvat'])))

if DEBUG:
    siglog_path = Path(__file__).parent.parent / 'work/siglog'
