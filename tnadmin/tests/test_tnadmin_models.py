import os
from pathlib import Path
import pytest
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from django.core import management
from tnadmin.models import *
from django.conf import settings
assert 'fedop' in settings.INSTALLED_APPS
assert 'tnadmin' in settings.INSTALLED_APPS

from tnadmin.tests.setup_db_tnadmin import load_tnadmin1, setup_db_tables_tnadmin


def test_gvorg_count(load_tnadmin1):
    assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'


def test_gvorg_get(load_tnadmin1):
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert o.gvouvkz == 'BMJ'


def test_gvFedOrg_insert(load_tnadmin1):
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    fedorg = GvFederationOrg(gvouid=o)
    fedorg.gvContractStatus = LEGAL_BASIS_PVV
    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
    fedorg.save()
