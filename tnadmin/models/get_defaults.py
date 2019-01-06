from tnadmin.models.constants import EMPTY_PARENT_ORG
from tnadmin.models.gvfederation import GvFederation
#from tnadmin.models.gvfederationorg import GvFederationOrg

def get_default_federationname() -> int:
    try:
        defaultFedName = GvFederation.objects.filter(gvDefaultFederation=True)[0].id
    except IndexError:
        defaultFedName = ''
    return defaultFedName


def get_default_org() -> int:
    # cannot get GvFederationOrg.objects.get(gvouid='AT:PVP:0') here -> hard code and make constant after
    # initial migration
    return EMPTY_PARENT_ORG

