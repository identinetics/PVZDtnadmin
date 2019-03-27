from pathlib import Path

import pytest
from django.core import management

from fedop.models.policystorage import PolicyStorage


#pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


def setup_db_tables_fedop():
    with open('/tmp/pvzdweb_fedop_testout_migratedb.log', 'w') as fd:
        management.call_command('migrate', 'fedop', stdout=fd)


def loaddata_fedop1():
    def add_policy_storage():
        polstore1_path = Path('fedop') / 'fixtures' / 'policystore1'
        ps = PolicyStorage()
        # ps.policy_journal_xml = polstore1_path / 'policydict.xml'.read_bytes()  # -> xmlsign=False
        ps.policy_dict_html = (polstore1_path / 'policydict.html').read_text()
        ps.policy_dict_json = (polstore1_path / 'policydict.json').read_text()
        ps.policy_journal_json = (polstore1_path / 'policyjournal.json').read_text()
        ps.shibacl = (polstore1_path / 'shibacl.xml').read_bytes()
        ps.trustedcerts_report = (polstore1_path / 'trustedcerts.txt').read_text()
        ps.save()
        pass

    fedop_data = Path('fedop/fixtures/fedop1.json')
    assert fedop_data.is_file(), f"could not find file {fedop_data}"
    management.call_command('loaddata', fedop_data)
    try:
        add_policy_storage()
    except Exception as e:
        raise e

