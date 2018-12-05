import os.path
from os.path import join as opj
import pytest
import django
from django.conf import settings
from django.http import HttpRequest
from django.test import RequestFactory

from portaladmin.constants import STATUS_REQUEST_QUEUE, STATUS_REJECTED
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path
from portaladmin.admin.mds_sign_and_update import mds_sign_and_update

pytestmark = pytest.mark.django_db  # allow test to access DB
path_expected_results = 'expected_results'


@pytest.fixture
def testdata_basedir():
    #return opj(settings.BASE_DIR, 'portaladmin', 'tests')
    return opj(settings.BASE_DIR, 'PVZDlib', 'PVZDpy', 'tests', 'testdata')


@pytest.fixture
def ed_path22(testdata_basedir):
    return ed_path(22, dir=opj(testdata_basedir, 'saml'))

# not a fixutre, re-evaluated per call
def fixture_get_idp22_qs():
    return MDstatement.objects.filter(entityID='https://idp22.identinetics.com/idp.xml',
                                      statusgroup='frontend')

#@pytest.fixture
#def result22_valmsg(testdata_basedir):
#    with open(opj(testdata_basedir, 'expected_results', 'result22_valmsg.json')) as fd:
#        return fd.read()

def test_insert22(ed_path22):
    def _delete_if_exists():
        mds = fixture_get_idp22_instance()
        if mds:
            mds[0].delete()
    def _insert_as_if_unsigned():
        with open(ed_path22) as fd:
            django_file = django.core.files.File(fd)
            mds = MDstatement()
            mds.ed_file_upload.save(os.path.basename(ed_path22), django_file, save=True)
        mds = fixture_get_idp22_qs()
        assert mds
    _delete_if_exists
    _insert_as_if_unsigned()


def test_sign22(ed_path22):
    with open(ed_path22) as fd:
        django_file = django.core.files.File(fd)
        mds = MDstatement()
        mds.ed_file_upload.save(os.path.basename(ed_path22), django_file, save=True)
    factory = RequestFactory()
    request = factory.get('/dummypath')
    queryset = fixture_get_idp22_qs()
    mds_sign_and_update(None, request, queryset, used_uploaded_as_signed=True, unittest=True)

    result = fixture_get_idp22_qs()[0]
    assert STATUS_REQUEST_QUEUE == result.status
    assert 'Rainer Hörbe' == result.signer_subject

