import os
import pathlib
import pytest
from tnadmin.models import *
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from django.conf import settings
from django.core import management
from pvzdweb.settings import *
INSTALLED_APPS=list(set(INSTALLED_APPS + ['fedop']))

#pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


@pytest.fixture(scope="module")
def setup_and_load_tnadmin1():
    management.call_command('migrate', 'tnadmin')
    tnadmin_data = pathlib.Path('tnadmin/fixtures/tnadmin1.json')
    assert tnadmin_data.is_file(), f'could not find file {tnadmin_data}'
    management.call_command('loaddata', tnadmin_data)


def test_gvorg_count(setup_and_load_tnadmin1):
    assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'


def test_gvorg_get(setup_and_load_tnadmin1):
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert o.gvouvkz == 'BMJ'


def test_gvFedOrg_insert(setup_and_load_tnadmin1):
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    fedorg = GvFederationOrg(gvouid=o)
    fedorg.gvContractStatus = LEGAL_BASIS_PVV
    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
    fedorg.save()