import os
from pathlib import Path
import pytest
import django
from django.conf import settings
from django.core import management
import django.core.files
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_pytest_dev")
django.setup()
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path

#pytestmark = pytest.mark.django_db  # not working for whatever reason.
                                     # workaround from https://github.com/pytest-dev/pytest-django/issues/396
from pytest_django.plugin import _blocking_manager
from django.db.backends.base.base import BaseDatabaseWrapper
_blocking_manager.unblock()
_blocking_manager._blocking_wrapper = BaseDatabaseWrapper.ensure_connection

path_expected_results = 'expected_results'

@pytest.fixture(scope="module")
def setup_db_tables():
    with open('/tmp/pvzdweb_padmin_testout_migratedb.log', 'w') as fd:
        management.call_command('migrate', 'fedop', stdout=fd)
        management.call_command('migrate', 'portaladmin', stdout=fd)


def assert_equal(expected, actual, fn=''):
    # workaround because pycharm does not display the full string (despite pytest -vv etc)
    msg = fn+"\n'"+actual+"' != '"+expected+"' "
    assert expected == actual, msg


def fixture_testdata_basedir():
    #return Path(settings.BASE_DIR / 'portaladmin' / 'tests' / 'saml'
    return Path(settings.BASE_DIR) / 'PVZDlib' / 'PVZDpy' / 'tests' / 'testdata' / 'saml'


def fixture_result(filename):
    p = Path(settings.BASE_DIR) / 'portaladmin' / 'tests' / path_expected_results / filename
    with p.open() as fd:
        return fd.read()


@pytest.mark.parametrize('expected_result_fn, ed_path_no',
                         [('insert01.json', 1),
                          ('insert02.json', 2),
                          ('insert03.json', 3),
                          ('insert04.json', 4),
                          ('insert05.json', 5),
                          ('insert06.json', 6),
                          ('insert07.json', 7),
                          ('insert08.json', 8),
                          ('insert09.json', 9),
                          ('insert10.json', 10),
                          ('insert11.json', 11),
                          ('insert12.json', 12),
                          ('insert13.json', 13),
                          ('insert14.json', 14),
                          ('insert15.json', 15),
                          # ('insert16.json', 16),   # causes unique contraint violation
                          # ('insert17.json', 17),   # causes unique contraint violation
                          ('insert18.json', 18),
                          ('insert19.json', 19),
                          # ('insert20.json', 20),   # causes unique contraint violation
                          ('insert21.json', 21),
                          ('insert22.json', 22),
                          ('insert23.json', 23),
                          ])
def test_insert(setup_db_tables, expected_result_fn, ed_path_no):
    fn = Path(ed_path(ed_path_no, dir=fixture_testdata_basedir()))
    with fn.open('rb') as fd:
        django_file = django.core.files.File(fd)
        mds = MDstatement()
        mds.ed_file_upload.save(fn.name, django_file, save=True)
    #assert 1 == len(MDstatement.objects.all())
    expected_result = fixture_result(expected_result_fn)
    assert_equal(expected_result, MDstatement.objects.all()[0].serialize_json())

#def test_unique_constraint() # TODO