import os
from pvzdweb.settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# temporary instance for automated tests

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'work', 'db.test.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'database', 'db.test.sqlite3'),
        },
    }
}


#MEDIA_ROOT = [
#    os.path.join(BASE_DIR, 'PVZDlib/PVZDpy/tests/testdata/saml'),
#]

PVZD_SETTINGS = {
    'policydir': 'saml/poldir1.json',
}