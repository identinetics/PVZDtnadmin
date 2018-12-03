# Notes: execute from Pycharm/run or CLI causes django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
# Work around: run from Pycharm/Python Console

from os.path import join as opj
from django.conf import settings
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path

#basedir = settings.BASE_DIR
basedir = '/Users/admin/devl/python/identinetics/PVZDweb'


def main():
    add_stpbetreiber()
    add_namespaces()
    add_userprivilege(s)


def poldir1_():
    return opj(settings.BASE_DIR, 'portaladmin', 'tests', 'saml')
    # return opj(settings.BASE_DIR, 'PVZDlib', 'PVZDpy', 'tests', 'testdata', 'saml', )


def add_stpbetreiber():
    org_recs = policystore1.get_all_orgids()

    for o in org_recs.keys():
        s = STPbetreiber()
        s.gvOuID = o
        s.cn = org_recs[o][0]
        s.save()


def add_namespaces():
    pass


def add_userprivilege(s):
    pass


main()



