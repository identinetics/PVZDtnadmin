import os
from pathlib import Path
import pytest
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from django.core import management

#pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


@pytest.fixture(scope="module")
def setup_db_tables_tnadmin():
    with open('/tmp/pvzdweb_fedop_testout_migratedb.log', 'w') as fd:
        management.call_command('migrate', 'tnadmin', stdout=fd)


@pytest.fixture(scope="module")
def load_tnadmin1(setup_db_tables_tnadmin):
    tnadmin_data = Path('tnadmin/fixtures/tnadmin1.json')
    assert tnadmin_data.is_file(), f'could not find file {tnadmin_data}'
    management.call_command('loaddata', tnadmin_data)
