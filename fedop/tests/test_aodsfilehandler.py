import json
import os
from pathlib import Path

import django
import pytest
from django.conf import settings

import common.pytest_django_db
from common.recreate_db import recreate_db
from PVZDpy.aodsfilehandler import AodsFileHandler
from fedop.tests.setup_db_fedop import loaddata_fedop1, setup_db_tables_fedop
from tnadmin.models.gvorg import GvOrganisation
from tnadmin.tests.setup_db_tnadmin import load_tnadmin1, setup_db_tables_tnadmin

# prepare database fixture
pytestmark = pytest.mark.unittest_db
django.setup()
assert 'fedop' in settings.INSTALLED_APPS
recreate_db() # drop/create db before django opens a connection
setup_db_tables_tnadmin()
setup_db_tables_fedop()
load_tnadmin1()
loaddata_fedop1()
assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'


@pytest.fixture
def testdata_dir() -> Path:
    return Path(__file__).parent / 'data' / 'aodsfh'


@pytest.fixture
def config_file(testdata_dir) -> None:
    os.environ['PVZDLIB_CONFIG_MODULE'] = str(testdata_dir / 'pvzdlib_config.py')


def test_create_read(config_file, testdata_dir):
    aodsfh = AodsFileHandler()
    aodsfh.remove()
    aods = {"AODS": [{"content":["header","","contentfields"],"delete": False}]}
    poldict_json = '{"domain": {}, "issuer": {}, "organization": {}, "revocation": {}, "userprivilege": {}}'
    aodsfh.save_journal(aods)
    aodsfh.save_policydict_json(poldict_json)
    aodsfh.save_policydict_html('<html/>')
    aodsfh.save_shibacl(b'<root/>')
    aodsfh.save_trustedcerts_report('some text')
    policyjournal = aodsfh.read()
    policyjournal_expected = testdata_dir / 'policyjournal_expected.json'
    assert policyjournal == json.load(policyjournal_expected.open())