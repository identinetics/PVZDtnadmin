import os.path
from os.path import join as opj
import pytest
import django.core.files
from django.conf import settings
from portaladmin.models import MDstatement
from PVZDpy.tests.common_fixtures import ed_path

pytestmark = pytest.mark.django_db
path_expected_results = 'expected_results'


def assert_equal(expected, actual, fn=''):
    # workaround because pycharm does not display the full string (despite pytest -vv etc)
    msg = fn+"\n'"+actual+"' != '"+expected+"' "
    assert expected == actual, msg

# work-around for lack of pytest's ability to use fixtures in @pytest.mark.parametrize
def fixture_testdata_basedir():
    #return opj(settings.BASE_DIR, 'portaladmin', 'tests', 'saml')
    return opj(settings.BASE_DIR, *['PVZDlib', 'PVZDpy', 'tests', 'testdata', 'saml', ])


# work-around for lack of pytest's ability to use fixtures in @pytest.mark.parametrize
def fixture_result(filename):
    with open(opj(settings.BASE_DIR, *['portaladmin', 'tests'], path_expected_results, filename)) as fd:
        return fd.read()


@pytest.mark.parametrize('expected_result_fn, ed_path_no',
                         [('insert01.json', 1),
                          ('insert02.json', 2),
                          ('insert03.json', 3),
                          ('insert04.json', 4),
                          ('insert05.json', 5),
                          ('insert06.json', 6),
                          ('insert07.json', 7),
                          ('insert08.json', 8),
                          ('insert09.json', 9),
                          ('insert10.json', 10),
                          ('insert11.json', 11),
                          ('insert12.json', 12),
                          ('insert13.json', 13),
                          ('insert14.json', 14),
                          ('insert15.json', 15),
                          ('insert16.json', 16),
                          ('insert17.json', 17),
                          ('insert18.json', 18),
                          ('insert19.json', 19),
                          ('insert20.json', 20),
                          ('insert21.json', 21),
                          ('insert22.json', 22),
                          ('insert23.json', 23),
                          ])
def test_insert(expected_result_fn, ed_path_no):
    fn = ed_path(ed_path_no, dir=fixture_testdata_basedir())
    with open(fn) as fd:
        django_file = django.core.files.File(fd)
        mds = MDstatement()
        mds.ed_file_upload.save(os.path.basename(fn), django_file, save=True)
    assert 1 == len(MDstatement.objects.all())
    expected_result = fixture_result(expected_result_fn)
    with open('/Users/admin/devl/python/identinetics/PVZDweb/portaladmin/tests/testout/'+os.path.basename(expected_result_fn), 'w') as fd:
        fd.write(MDstatement.objects.all()[0].serialize_json())
    assert_equal(expected_result, MDstatement.objects.all()[0].serialize_json())

#def test_unique_constraint() # TODO