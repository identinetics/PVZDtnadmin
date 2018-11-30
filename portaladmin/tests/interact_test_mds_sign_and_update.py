from os.path import join as opj
import pytest
from django.conf import settings
from django.http import HttpRequest

from portaladmin.constants import STATUS_REQUEST_QUEUE, STATUS_REJECTED
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path
from portaladmin.admin.mds_sign_and_update import mds_sign_and_update

pytestmark = pytest.mark.django_db
path_expected_results = 'expected_results'


@pytest.fixture
def testdata_basedir():
    return opj(settings.BASE_DIR, 'portaladmin', 'tests')
    # return opj(settings.BASE_DIR, *['PVZDlib', 'PVZDpy', 'tests', 'testdata'])


@pytest.fixture
def ed_path06(testdata_basedir):
    return ed_path(6, dir=opj(testdata_basedir, 'saml'))


@pytest.fixture
def result06_valmsg(testdata_basedir):
    with open(opj(testdata_basedir, 'expected_results', 'result06_valmsg.json')) as fd:
        return fd.read()

def test_insert06(ed_path06, result06_valmsg):
    mds = MDstatement(ed_file_upload=ed_path06)
    mds.save()
    queryset = MDstatement.objects.all()
    assert 1 == len(queryset)
    request = HttpRequest()
    mds_sign_and_update(None, request, queryset)
    result = MDstatement.objects.all()[0]

    assert result.ed_signed
    assert STATUS_REJECTED == result.status
    assert 'Rainer Hörbe' == result.signer_subject
    assert result06_valmsg == result.validation_message
    pass
