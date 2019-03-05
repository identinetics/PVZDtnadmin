import os
from pathlib import Path
import pytest
import django
import coreapi
from portaladmin.constants import STATUSGROUP_FRONTEND
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path
from django.conf import settings
assert 'portaladmin' in settings.INSTALLED_APPS

pytestmark = pytest.mark.django_db

import django.core.files
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_dev")
django.setup()

path_expected_results = 'expected_results'

def assert_equal(expected, actual, fn=''):
    # workaround because pycharm does not display the full string (despite pytest -vv etc)
    msg = fn+"\n'"+actual+"' != '"+expected+"' "
    assert expected == actual, msg


def fixture_testdata_basedir():
    return Path(settings.BASE_DIR) / 'PVZDlib' / 'PVZDpy' / 'tests' / 'testdata' / 'saml'


def fixture_result(filename):
    p = Path(settings.BASE_DIR) / 'portaladmin' / 'tests' / path_expected_results / filename
    with p.open() as fd:
        return fd.read()


def test_api_update_ed_signed():
    ''' update ed_signed via API
        requires PVZDweb runnning on dev database (no fixture yet for this)
    '''
    fn = Path(ed_path(22, dir=fixture_testdata_basedir()))
    with fn.open('rb') as fd:
        django_file = django.core.files.File(fd)
        mds = MDstatement()
        count = MDstatement.objects.filter(entityID='https://idp22.identinetics.com/idp.xml', statusgroup=STATUSGROUP_FRONTEND)
        if count:
            mds = MDstatement.objects.get(entityID='https://idp22.identinetics.com/idp.xml', statusgroup=STATUSGROUP_FRONTEND)
            mds.ed_signed = ''
            mds.save()
        else:
            django_file = django.core.files.File(fd)
            mds = MDstatement()
            mds.ed_file_upload.save(fn.name, django_file, save=True)
        update_id = mds.id

    client = coreapi.Client()
    schema = client.get("http://localhost:8000/docs/")

    action = ["mdstatement", "partial_update"]
    params = {
        "id": update_id,
        "admin_note": "Updated ed_signed from REST API",
        "ed_signed": fn.read_text(),
    }
    result = client.action(schema, action, params=params)
    #expected_result = fixture_result('insert22.json')
    #assert_equal(expected_result, MDstatement.objects.all()[0].serialize_json())

