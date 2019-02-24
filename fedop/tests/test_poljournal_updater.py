import json
import os
from pathlib import Path
import pytest
import enforce
assert os.environ['DJANGO_SETTINGS_MODULE'] in ('pvzdweb.settings_pytest_dev', 'pvzdweb.settings_pytest'), \
    'require in-memory-db for loading fixtures'
from django.core import management
from pvzdweb.settings import *
INSTALLED_APPS=list(set(INSTALLED_APPS + ['fedop']))

from fedop.models import Issuer, Namespaceobj, PolicyStorage, Revocation, Userprivilege
from fedop.poljournal_updater import PolicyJournalUpdater

# pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                      # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


@pytest.fixture(scope='module')
def load_schema():
    management.call_command('migrate')


@pytest.fixture(scope='module')
def load_tnadmin1():
    tnadmin_data = Path('tnadmin/fixtures/tnadmin1.json')
    assert tnadmin_data.is_file(), f"could not find file {tnadmin_data}"
    management.call_command('loaddata', tnadmin_data)


@pytest.fixture(scope='module')
def load_fedop1(load_schema, load_tnadmin1):
    fedop_data = Path('fedop/fixtures/fedop1.json')
    assert fedop_data.is_file(), f"could not find file {fedop_data}"
    management.call_command('loaddata', fedop_data)
    # canot json-represent the poljournal, therefore load_changelist it from file
    fedop_policyjournal = Path('fedop/fixtures/poljournal_testdata.xml')
    ps = PolicyStorage.objects.get(id=1)
    with fedop_policyjournal.open('rb') as fd:
        ps.policy_journal = fd.read()
    ps.save()


@pytest.fixture
def testdata_dir() -> Path:
    return Path(__file__).parent / 'data' / 'poljournalupd'


@pytest.fixture
def pvzdconfig():
    conf_path = Path(__file__).parent.parent / 'config' / 'pvzdlib_config.py'
    os.environ['PVZDLIB_CONFIG_MODULE'] = str(conf_path)


enforce.config({'enabled': True, 'mode': 'covariant'})


@enforce.runtime_validation
def test_poljournal_updater(load_fedop1, testdata_dir, pvzdconfig):
    policy_journal_updater = PolicyJournalUpdater()
    policy_journal_updater.load_changelist()
    ps = policy_journal_updater.policy_dict
    with (testdata_dir / 'expected_result' / 'polstore.json').open() as fd:
        assert ps.get_policydict() == json.load(fd)
