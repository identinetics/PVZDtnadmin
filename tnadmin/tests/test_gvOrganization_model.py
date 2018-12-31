import os.path
from os.path import join as opj
#import pytest
#from django.conf import settings
from tnadmin.models import GvOrganisation

pytestmark = pytest.mark.django_db
#path_expected_results = 'expected_results'


def test_query():
    o = GvOrganisation.objects.filter(gvOuId='AT:TEST:1'')