import os
import pytest
import sys

import django
if __name__ == '__main__':
    django_proj_path = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(django_proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoldap.settings")
django.setup()
from ldapgvat.models import GvOrganisation

pytestmark = pytest.mark.django_db

print('test django-ldapdb')


def test_gvOrganisation_get_by_gvouid():
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert 'active' == o.gvStatus

def test_gvOrganisation_get_by_dn():
    o = GvOrganisation.objects.get(dn='gvOuId=AT:B:1,dc=at')
    assert 'active' == o.gvStatus

def test_gvOrganisation_update():
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert 'active' == o.gvStatus
    o.gvOtherID = 'test value'
    o.save()
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert 'test value' == o.gvOtherID

def test_gvOrganisation_query_exclude():
    assert 0 < GvOrganisation.objects.all().exclude(gvouid__startswith='AT:B:')
