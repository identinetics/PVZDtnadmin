import datetime

import pytest
import django
from django.conf import settings

from common.recreate_db import recreate_db
from tnadmin.models.gvfederationorg import GvFederationOrg
from tnadmin.models.gvorg import GvOrganisation
from tnadmin.models.constants import LEGAL_BASIS_PVV
from tnadmin.tests.setup_db_tnadmin import load_tnadmin1, setup_db_tables_tnadmin

# prepare database fixture (a temporary in-memory database is created for this test)
pytestmark = pytest.mark.unittest_db
django.setup()
assert 'tnadmin' in settings.INSTALLED_APPS
recreate_db() # drop/create db before django opens a connection
setup_db_tables_tnadmin()
load_tnadmin1()
assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'


@pytest.mark.unittest_db
def test_gvorg_count():
    assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'


@pytest.mark.unittest_db
def test_gvorg_get():
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert o.gvouvkz == 'BMJ'


@pytest.mark.unittest_db
def test_gvFedOrg_insert():
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    fedorg = GvFederationOrg(gvouid=o)
    fedorg.gvContractStatus = LEGAL_BASIS_PVV
    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
    fedorg.save()
