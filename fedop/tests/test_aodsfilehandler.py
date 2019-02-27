import json
import os
from pathlib import Path
import pytest
from django.conf import settings
from PVZDpy.aodsfilehandler import AodsFileHandler
from PVZDpy.userexceptions import ValidationError, UnauthorizedAODSSignerError

from pvzdweb.settings import *
INSTALLED_APPS=list(set(INSTALLED_APPS + ['fedop']))
from .setup_djangodb import *


@pytest.fixture
def testdata_dir() -> Path:
    return Path(__file__).parent / 'data' / 'aodsfh'


@pytest.fixture
def config_file(testdata_dir) -> None:
    os.environ['PVZDLIB_CONFIG_MODULE'] = str(testdata_dir / 'pvzdlib_config.py')


def test_create_read(config_file, setup_db_tables, testdata_dir):
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