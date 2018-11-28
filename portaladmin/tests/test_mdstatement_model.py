from os.path import join as opj
import pytest
from django.conf import settings
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path

pytestmark = pytest.mark.django_db

@pytest.fixture
def ed_path1():
    return ed_path(1, dir=opj(settings.BASE_DIR, 'portaladmin/tests/saml'))

def test_insert01(ed_path1):
    mds = MDstatement(ed_file_upload=ed_path1)
    mds.save()
    assert 1 == len(MDstatement.objects.all())
    pass