import json
import logging
import os
from pathlib import Path
import pytest
import enforce
from PVZDpy.aods_record import AodsRecord
from PVZDpy.policychange import PolicyChangeList
from fedop.models import Issuer, Namespaceobj, PolicyStorage, Revocation, Userprivilege
from fedop.poljournal_updater import PolicyJournalUpdater
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


@pytest.fixture(scope='module')
def load_fedop1(setup_db_tables_fedop, loaddata_fedop1):
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
@pytest.mark.standalone_only
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
    # preview(policy_change_list)
    policy_journal_updater.append_poljournal()
    assert len(policy_change_list.changelist) == 22
    policy_store = policy_journal_updater.policy_dict
    with (testdata_dir / 'expected_result' / 'polstore01.json').open() as fd:
        assert policy_store.get_policydict() == json.load(fd)
