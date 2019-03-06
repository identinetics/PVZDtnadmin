import os
from pathlib import Path
import pytest
import requests
from portaladmin.constants import STATUSGROUP_FRONTEND
from portaladmin.models import MDstatement
from portaladmin.views import _get_sigproxy_url
from django.conf import settings
assert 'portaladmin' in settings.INSTALLED_APPS

pytestmark = pytest.mark.django_db
import django.core.files
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_dev")
django.setup()


def assert_equal(expected, actual, fn=''):
    # workaround because pycharm does not display the full string (despite pytest -vv etc)
    msg = str(fn) + "\n'" + actual + "' != '" + expected + "' "
    assert actual == expected, msg


@pytest.fixture()
def testdata_dir() -> Path:
    return Path(settings.BASE_DIR) / 'portaladmin' / 'tests' / 'testdata' / 'sign_sigproxy'


@pytest.fixture()
def config_file() -> None:
    os.environ['PVZDLIB_CONFIG_MODULE'] = str(Path(settings.BASE_DIR)  / 'fedop/config/pvzdlib_config.py')


@pytest.fixture()
def ed_prepared_in_db(testdata_dir) -> int:
    ed_unsigned_fp = testdata_dir / '01_idp1_valid_cert.xml'
    with ed_unsigned_fp.open('rb') as fd:
        django_file = django.core.files.File(fd)
        mds = MDstatement()
        count = MDstatement.objects.filter(entityID='https://idp1.identinetics.com/idp.xml', statusgroup=STATUSGROUP_FRONTEND)
        if count:
            mds = MDstatement.objects.get(entityID='https://idp1.identinetics.com/idp.xml', statusgroup=STATUSGROUP_FRONTEND)
            mds.ed_signed = ''
            mds.save()
        else:
            django_file = django.core.files.File(fd)
            mds = MDstatement()
            mds.ed_file_upload.save(ed_unsigned_fp.name, django_file, save=True)
        return mds.id


@pytest.mark.requires_webapp
def test_get_sigproxyurl(config_file, testdata_dir, ed_prepared_in_db):
    expected_result_fp = testdata_dir / 'expected_results' / 'sigproxy_client.html'
    expected_result_html = expected_result_fp.read_text()
    url = _get_sigproxy_url(settings.PVZD_ORIGIN + '/admin/portaladmin/mdstatement/', 1)
    response = requests.get(url)
    assert_equal(expected_result_html, response.text, expected_result_fp)
