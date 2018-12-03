# Notes: execute from Pycharm/run or CLI causes django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
# Work around: run from Pycharm/Python Console

from os.path import join as opj
from django.conf import settings
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path

#basedir = settings.BASE_DIR
basedir = '/Users/admin/devl/python/identinetics/PVZDweb'



def fixture_testdata_basedir():
    return opj(settings.BASE_DIR, 'portaladmin', 'tests', 'saml')
    # return opj(settings.BASE_DIR, *['PVZDlib', 'PVZDpy', 'tests', 'testdata', 'saml', ])


for testno in range(1, 23):
    edp = ed_path(testno, dir=fixture_testdata_basedir())
    mds = MDstatement(ed_file_upload=edp, admin_note='load_db')
    mds.save()


def sign04():
    qs = MDstatement.objects.filter(entityID='https://idp4.example.com/idp.xml',
                                    statusgroup='frontend')
    mds = qs[0]
    mds.ed_signed = mds.ed_uploaded
    mds.status = STATUS_SIGNATURE_APPLIED
    mds.save(operation='mds_sign_and_update')