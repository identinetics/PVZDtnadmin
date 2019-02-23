import json
import os
from pathlib import Path
import pytest

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from django.conf import settings
from django.core import management
from pvzdweb.settings import *
INSTALLED_APPS=list(set(INSTALLED_APPS + ['fedop']))

from PVZDpy.config.appconfig_abstract import PVZDlibConfigAbstract
from PVZDpy.trustedcerts import TrustedCerts
from PVZDpy.userexceptions import PolicyJournalNotInitialized

#pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


@pytest.fixture(scope="module")
def setup_db_tables():
    management.call_command('migrate', 'tnadmin')
    management.call_command('migrate', 'fedop')


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


# --- 01 ---

def test_01_default_not_init():
    pvzdconf = PVZDlibConfigAbstract.get_config()
    backend = pvzdconf.polstore_backend
    with pytest.raises(PolicyJournalNotInitialized) as context:
        _ = backend.get_policy_journal_json()


# --- 02 ---

@pytest.fixture
def expected_poldict_json02(testdata_dir):
    p = testdata_dir/ 'expected_results' / 'policy_journal02.json'
    return json.load(p.open())


#def test_02_read_existing(pvzdconfig02, expected_poldict_json02):
#    pvzdconf = PVZDlibConfigAbstract.get_config()
#    backend = pvzdconf.polstore_backend
#    policy_journal_json = backend.get_policy_journal_json()
#    assert json.loads(policy_journal_json) == expected_poldict_json02


# --- 03 ---

def test_03_initialize(config_file, setup_db_tables):
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
