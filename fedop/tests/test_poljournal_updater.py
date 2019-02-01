import os
import pathlib
import pytest
assert os.environ["DJANGO_SETTINGS_MODULE"] in ("pvzdweb.settings_pytest_dev", "pvzdweb.settings_pytest"), \
    "require in-memory-db for loading fixtures"

from django.core import management
from pvzdweb.settings import *
INSTALLED_APPS=list(set(INSTALLED_APPS + ['fedop']))

from fedop.models.issuer import Issuer
from fedop.models.namespace import Namespaceobj
from fedop.models.policy_journal import PolicyJournal
from fedop.models.revocation import Revocation
from fedop.models.userprivilege import Userprivilege
from fedop.poljournal_updater import PolicyJournalUpdater

pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


@pytest.fixture(scope="module")
def load_tnadmin1():
    management.call_command('migrate')
    tnadmin_data = pathlib.Path('tnadmin/fixtures/tnadmin1.json')
    assert tnadmin_data.is_file(), f'could not find file {tnadmin_data}'
    management.call_command('loaddata', tnadmin_data)

@pytest.fixture(scope="module")
def load_fedop1(load_tnadmin1):
    management.call_command('migrate')
    fedop_data = pathlib.Path('fedop/fixtures/fedop1.json')
    assert fedop_data.is_file(), f'could not find file {fedop_data}'
    management.call_command('loaddata', fedop_data)
    # canot json-represent the poljournal, therofre load it from file
    fedop_policyjournal = pathlib.Path('fedop/fixtures/poljournal_empty1.xml')
    pj = PolicyJournal.objects.get(id=1)
    with fedop_policyjournal.open('rb') as fd:
        pj.policy_journal = fd.read()
    pj.save()

def test_poljournal_updater(load_fedop1):
    policy_journal_updater = PolicyJournalUpdater()
    policy_journal_updater.main()

