import json
import logging
import os
from pathlib import Path
import pytest
import enforce
from PVZDpy.aods_record import AodsRecord
from PVZDpy.policychange import PolicyChangeList
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
    logging.basicConfig(level=logging.DEBUG)
    fedop_data = Path('fedop/fixtures/fedop1.json')
    assert fedop_data.is_file(), f"could not find file {fedop_data}"
    management.call_command('loaddata', fedop_data)
    # canot json-represent the poljournal, therefore get_changelist it from file
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
def test_poljournal_updater01(capfd, load_fedop1, testdata_dir, pvzdconfig):
    def preview(changelist: PolicyChangeList):
        with capfd.disabled():   # disable pytest output capture
            i = 0
            for changeitem in changelist.changelist:
                i += 1
                print(AodsRecord(changeitem))
            print(f"processed {i} change items")


    policy_journal_updater = PolicyJournalUpdater()
    policy_change_list = policy_journal_updater.get_changelist()
    preview(policy_change_list)
    policy_journal_updater.append_poljournal()
    assert len(policy_change_list.changelist) == 19
    policy_store = policy_journal_updater.policy_dict
    with (testdata_dir / 'expected_result' / 'polstore01.json').open() as fd:
        assert policy_store.get_policydict() == json.load(fd)
