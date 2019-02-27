import json
import logging
import os
from pathlib import Path
import pytest
import enforce
from PVZDpy.aods_record import AodsRecord
from PVZDpy.policychange import PolicyChangeList
from django.core import management
from fedop.models import Issuer, Namespaceobj, PolicyStorage, Revocation, Userprivilege
from fedop.poljournal_updater import PolicyJournalUpdater

from pvzdweb.settings import *
INSTALLED_APPS=list(set(INSTALLED_APPS + ['fedop']))
from .setup_djangodb import *


@pytest.fixture(scope='module')
def load_fedop1(setup_db_tables, loaddata_fedop1):
    logging.basicConfig(level=logging.DEBUG)
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
