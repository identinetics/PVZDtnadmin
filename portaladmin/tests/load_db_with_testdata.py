# Notes: execute from Pycharm/run or CLI causes django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
# Work around: run from Pycharm/Python Console

from os.path import join as opj
from PVZDpy.tests.common_fixtures import ed_path

import django
import sys
import os

if __name__ == '__main__':
    django_proj_path = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(django_proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
    django.setup()
else:
    assert False

from portaladmin.models import MDstatement
from django.conf import settings

#basedir = settings.BASE_DIR
basedir = '/Users/admin/devl/python/identinetics/PVZDweb'


def fixture_testdata_basedir():
    return opj(settings.BASE_DIR, 'portaladmin', 'tests', 'saml')
    # return opj(settings.BASE_DIR, *['PVZDlib', 'PVZDpy', 'tests', 'testdata', 'saml,', ])


for testno in range(1, 23):
    fn = ed_path(testno, dir=fixture_testdata_basedir())
    with open(fn) as fd:
        django_file = django.core.files.File(fd)
        mds = MDstatement(admin_note='load_db_with_testdata')
        mds.ed_file_upload.save(os.path.basename(fn), django_file, save=False)
    qs = MDstatement.objects.filter(
        entityID=mds.entityID,
        make_blank_entityid_unique=mds.make_blank_entityid_unique,
        statusgroup=mds.statusgroup  )
    if not qs:
        try:
            mds.save()
            print('added MDStatement for %s' % os.path.basename(fn))
        except Exception as e:
            print('failed to add MDStatement for {}. {}'.format(os.path.basename(fn), e))
    else:
        print('skipped MDStatement for %s' % os.path.basename(fn))


def sign04():
    qs = MDstatement.objects.filter(entityID='https://idp4.example.com/idp.xml',
                                    statusgroup='frontend')
    mds = qs[0]
    mds.ed_signed = mds.ed_uploaded
    mds.status = STATUS_SIGNATURE_APPLIED
    try:
        mds.save(operation='mds_sign_and_update')
        print('signed MDStatement for https://idp4.example.com/idp.xml')
    except Exception as e:
        print('failed to sign MDStatement for https://idp4.example.com/idp.xml\n' + e)
