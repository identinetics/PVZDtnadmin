import os
from pvzdweb.settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

INSTALLED_APPS=sorted(list(set(INSTALLED_APPS + ['fedop', 'ldapgvat', 'portaladmin', 'tnadmin'])))

PVZD_SETTINGS = {
    'logfilepep': opj(*'PVZDlib/PVZDpy/tests/testdout/pep.log'.split('/')),
    'loglevelpep': logging.DEBUG,
    'loglevelweb': logging.DEBUG,
    'pepoutdir': opj(*'PVZDlib/PVZDpy/tests/testout/pepout'.split('/')),
    'poldirhtml': opj(*'PVZDlib/PVZDpy/tests/testout/poldir/poldir.html'.split('/')),
    'poldirjson': opj(*'PVZDlib/PVZDpy/tests/testout/poldir/poldir.json'.split('/')),
    'policydir': opj(BASE_DIR, *'PVZDlib/PVZDpy/tests/testdata/saml/poldir1.json'.split('/')),
    'policyjournal': opj(*'PVZDlib/PVZDpy/tests/testdata/aodsfilehandler/pol_journal_sig_rh.xml'.split('/')),
    'regauthority': 'AG-IZ Testfed',
    'shibacl': opj(*'PVZDlib/PVZDpy/tests/testdout/poldir/shibacl.xml'.split('/')),
    'superuser': True,  # allow signer in trustedcerts to skip authorization check
    'trustedcerts': opj(*'PVZDlib/PVZDpy/tests/testdata/aodsfilehandler/trustedcerts_rh.json'.split('/')),
}
