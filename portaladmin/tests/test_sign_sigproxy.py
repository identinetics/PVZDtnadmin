import os
import re
import subprocess
from pathlib import Path

import django
import pytest
import requests

from portaladmin.constants import STATUSGROUP_FRONTEND
from portaladmin.models import MDstatement
from portaladmin.views import getstarturl

# prepare database fixture (a temporary in-memory database is created for this test)
# drop/create db before django opens a connection
subprocess.call(['ssh', 'devl11', '/home/r2h2/devl/docker/c_pvzdweb_pgnofsync/drop_createdb.sh'])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_dev")
from django.conf import settings
assert 'portaladmin' in settings.INSTALLED_APPS
django.setup()
from portaladmin.tests.setup_db_portaladmin import setup_db_tables_portaladmin


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
def test_get_sigproxyurl(config_file, setup_db_tables_portaladmin, testdata_dir, ed_prepared_in_db):
    expected_result_fp = testdata_dir / 'expected_results' / 'sigproxy_client.html'
    expected_result_html = expected_result_fp.read_text()
    url = getstarturl(1)
    response = requests.get(url)
    e_without_uniq_str = re.sub(r'    const csrftoken4proxy = ".*\n', '', expected_result_html)
    a_without_uniq_str = re.sub(r'    const csrftoken4proxy = ".*\n', '', response.text)
    assert a_without_uniq_str == e_without_uniq_str
