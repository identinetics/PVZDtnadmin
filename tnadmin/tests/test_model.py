import pytest
from tnadmin.models import *

pytestmark = pytest.mark.django_db


def test_gvorg_count():
    assert len(GvOrganisation.objects.all()) > 0, 'No gvOrganisation data found'

def test_gvorg_get():
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    assert o.gvouvkz == 'BMJ'

def test_gvFedOrg_insert():
    o = GvOrganisation.objects.get(gvouid='AT:B:1')
    fedorg = GvFederationOrg(gvouid=o)
    fedorg.gvContractStatus = LEGAL_BASIS_PVV
    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
    fedorg.save()