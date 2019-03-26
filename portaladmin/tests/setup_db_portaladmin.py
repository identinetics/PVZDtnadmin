import pytest
from django.core import management


#pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection


@pytest.fixture(scope="module")
def setup_db_tables_portaladmin():
    with open('/tmp/pvzdweb_portaladmin_testout_migratedb.log', 'w') as fd:
        management.call_command('migrate', 'portaladmin', stdout=fd)
