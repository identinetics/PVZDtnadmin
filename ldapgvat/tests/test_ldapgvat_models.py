import os
import pytest

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from ldapgvat.models import GvOrganisation


#@pytest.mark.django_db does not work
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection

@pytest.mark.requires_ldap
def test_gvOrganisation_get_by_gvouid():
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert 'active' == o.gvStatus


# get by dn is broken
# def test_gvOrganisation_get_by_dn():
#    o = GvOrganisation.objects.get(dn='gvOuId=AT:B:1,dc=at')
#    assert 'active' == o.gvStatus


# update is broken
# def test_gvOrganisation_update():
#    o = GvOrganisation.objects.get(gvouid='AT:B:1')
#    assert 'active' == o.gvStatus
#    o.gvOtherID = 'test value'
#    o.save()
#    o = GvOrganisation.objects.get(gvouid='AT:B:1')
#    assert 'test value' == o.gvOtherID


def test_gvOrganisation_query_exclude():
    assert 0 < len(GvOrganisation.objects.all().exclude(gvouid__startswith='AT:B:'))
