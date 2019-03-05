import json
import os
from pathlib import Path
import pytest
from PVZDpy.aodsfilehandler import AodsFileHandler
from tnadmin.models import GvOrganisation
from django.conf import settings
assert 'fedop' in settings.INSTALLED_APPS

# prepare database fixture (a temporary in-memory database is created for this test)
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from tnadmin.tests.setup_db_tnadmin import load_tnadmin1, setup_db_tables_tnadmin
def test_assert_tnadmin_loaded(load_tnadmin1):
    assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'
from fedop.tests.setup_db_fedop import loaddata_fedop1, setup_db_tables_fedop


@pytest.fixture
def testdata_dir() -> Path:
    return Path(__file__).parent / 'data' / 'aodsfh'


@pytest.fixture
def config_file(testdata_dir) -> None:
    os.environ['PVZDLIB_CONFIG_MODULE'] = str(testdata_dir / 'pvzdlib_config.py')


@pytest.mark.standalone_only
def test_create_read(config_file, setup_db_tables_fedop, testdata_dir):
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