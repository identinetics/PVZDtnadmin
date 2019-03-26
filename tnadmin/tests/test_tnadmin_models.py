import os
# from pathlib import Path
import pytest
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from tnadmin.models import *
from django.conf import settings
assert 'tnadmin' in settings.INSTALLED_APPS

# prepare database fixture (a temporary in-memory database is created for this test)
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from tnadmin.tests.setup_db_tnadmin import load_tnadmin1, setup_db_tables_tnadmin


@pytest.mark.standalone_db
def test_gvorg_count(load_tnadmin1):
    assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'


@pytest.mark.standalone_db
def test_gvorg_get(load_tnadmin1):
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert o.gvouvkz == 'BMJ'


@pytest.mark.standalone_db
def test_gvFedOrg_insert(load_tnadmin1):
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    fedorg = GvFederationOrg(gvouid=o)
    fedorg.gvContractStatus = LEGAL_BASIS_PVV
    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
    fedorg.save()
