#import os.path
from pathlib import Path

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
import django
django.setup()
from portaladmin.models import MDstatement
from django.conf import settings


def testdata_basedir():
    return Path(settings.BASE_DIR, 'portaladmin', 'tests', 'testdata')

def entities() -> Path:
    for file in testdata_basedir().glob('*'):
        if file.is_file():
            yield file

for entity in entities():
    with entity.open('rb') as fd:
        django_file = django.core.files.File(fd)
        mds = MDstatement(admin_note='load_db_with_testdata')
        mds.ed_file_upload.save(entity.name, django_file, save=False)
    qs = MDstatement.objects.filter(
        entityID=mds.entityID,
        make_blank_entityid_unique=mds.make_blank_entityid_unique,
        statusgroup=mds.statusgroup  )
    if not qs:
        try:
            mds.save()
            print('added MDStatement for %s' % entity.name)
        except Exception as e:
            print('skipped MDStatement for {}. {}'.format(entity.name, e))
    else:
        print('skipped MDStatement for %s' % entity.name)


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
