from os.path import join as opj
import pytest
from django.conf import settings
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path

pytestmark = pytest.mark.django_db
path_expected_results = 'expected_results'


def assert_equal(expected, actual, fn=''):
    # workaround because pycharm does not display the full string (despite pytest -vv etc)
    msg = fn+"\n'"+actual+"' != '"+expected+"' "
    assert expected == actual, msg


@pytest.fixture
def ed_path01():
    path = opj(settings.BASE_DIR, 'portaladmin', 'tests', 'saml')
    return ed_path(1, dir=path)
    # return opj(settings.BASE_DIR, *['PVZDlib', 'PVZDpy', 'tests', 'testdata', 'saml', 'unsigned_ed', '01_idp1_valid_cert.xml'])


@pytest.fixture
def result01():
    with open(opj(settings.BASE_DIR, *['portaladmin', 'tests'], path_expected_results, 'insert01.json')) as fd:
        return fd.read()


def test_insert01(ed_path01, result01):
    settings1 = settings
    mds = MDstatement(ed_file_upload=ed_path01)
    mds.save()
    assert 1 == len(MDstatement.objects.all())
    assert_equal(result01, MDstatement.objects.all()[0].serialize_json())
    pass


@pytest.fixture
def ed_path02():
    return ed_path(2, dir=opj(settings.BASE_DIR, 'portaladmin/tests/saml'))


@pytest.fixture
def result02():
    with open(opj(path_expected_results, 'insert02.json')) as fd:
        return fd.read()

# def test_insert02(ed_path02, result02):
#     mds = MDstatement(ed_file_upload=ed_path02)
#     mds.save()
#     assert 1 == len(MDstatement.objects.all())
#     assert_equal(result02, MDstatement.objects.all()[0].serialize_json())
#     pass