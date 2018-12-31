import django
import os
import pytest
import random
import sys
if __name__ == '__main__':
    django_proj_path = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(django_proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoldap.settings")
django.setup()
from ldapgvat.models import *

pytestmark = pytest.mark.django_db

print('test django-ldapdb')


def test_gvOrganisation_get_by_dn():
    o = gvOrganisation.objects.get(dn='gvOuId=AT:TEST:1,dc=gv,dc=at')
    assert o.gvStatus == 'active'

def test_gvOrganisation_get_by_gvouid():
    o = gvOrganisation.objects.get(gvOuId='AT:TEST:1')
    assert o.gvStatus == 'active'

