import json
import os
from pathlib import Path

import django
import pytest

from PVZDpy.config.pvzdlib_config_abstract import PVZDlibConfigAbstract
from PVZDpy.trustedcerts import TrustedCerts
from PVZDpy.userexceptions import PolicyJournalNotInitialized
from tnadmin.models import GvOrganisation
from django.conf import settings
assert 'fedop' in settings.INSTALLED_APPS

# prepare database fixture (a temporary in-memory database is created for this test)
pytest.mark.standalone_only
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from tnadmin.tests.setup_db_tnadmin import load_tnadmin1, setup_db_tables_tnadmin
def test_assert_tnadmin_loaded(load_tnadmin1):
    assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'
from fedop.tests.setup_db_fedop import loaddata_fedop1, setup_db_tables_fedop


@pytest.fixture(scope='module')
def config_file() -> None:
    os.environ['PVZDLIB_CONFIG_MODULE'] = str(Path(__file__).parent / 'data' / 'pvzdlib_config' / 'pvzdlib_config.py')


@pytest.fixture
def testdata_dir() -> Path:
    dir = Path('data/pvzdlib_config')
    dir.mkdir(parents=True, exist_ok=True)
    return dir


@pytest.fixture
def testout_dir() -> Path:
    dir = Path('testout/pvzdlib_config')
    dir.mkdir(parents=True, exist_ok=True)
    return dir

from .common import test_info

# --- 01 ---

# removed, because db setup now addes a dummy entry
# @pytest.mark.standalone_only
# def test_01_default_not_init(config_file):
#    pvzdconf = PVZDlibConfigAbstract.get_config()
#    backend = pvzdconf.polstore_backend
#    with pytest.raises(PolicyJournalNotInitialized) as context:
#        _ = backend.get_policy_journal_json()


# --- 02 ---

@pytest.fixture
def expected_poldict_json02(config_file, testdata_dir):
    p = testdata_dir/ 'expected_results' / 'policy_journal02.json'
    return json.load(p.open())


# @pytest.mark.standalone_only
# def test_02_read_existing(pvzdconfig02, expected_poldict_json02):
#    pvzdconf = PVZDlibConfigAbstract.get_config()
#    backend = pvzdconf.polstore_backend
#    policy_journal_json = backend.get_policy_journal_json()
#    assert json.loads(policy_journal_json) == expected_poldict_json02


# --- 03 ---

@pytest.mark.standalone_only
def test_03_initialize(config_file, setup_db_tables_fedop):
    pvzdconf = PVZDlibConfigAbstract.get_config()
    backend = pvzdconf.polstore_backend
    try:
        pvzdconf.polstore_backend.reset_pjournal_and_derived()
    except PolicyJournalNotInitialized:  # customize this to actual storage
        pass

    backend.set_policy_journal_xml(b'0')
    backend.set_policy_journal_json('{"journaltestentry": ""}')
    backend.set_poldict_json('{"dicttestentry": ""}')
    backend.set_poldict_html('<html/>')
    backend.set_shibacl(b'1')
    backend.set_trustedcerts_report('lore ipsum')
    assert backend.get_policy_journal_xml() == b'0'
    assert backend.get_policy_journal_json() == '{"journaltestentry": ""}'
    assert backend.get_poldict_json() == '{"dicttestentry": ""}'
    assert backend.get_poldict_html() == '<html/>'
    assert backend.get_shibacl() == b'1'
    assert backend.get_trustedcerts_report() == 'lore ipsum'
    assert backend.get_policy_journal_path().is_file()


