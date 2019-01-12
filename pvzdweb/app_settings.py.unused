from PVZDpy.invocation.aodsfhinvocation import aodsfhInvocation
from PVZDpy.invocation.aodslhinvocation import aodslhInvocation
from pvzdweb.settings import PVZD_SETTINGS


def get_aodsfhInvocation(aods_filename, trustedcerts_filename):
    return aodsfhInvocation(
        journal =      PVZD_SETTINGS['policyjournal'],
        trustedcerts = PVZD_SETTINGS['trustedcerts']
    )


def get_aodslhInvocation(journal = None,
                         poldirhtml = None,
                         poldirjson = None,
                         shibacl = None,
                         trustedcerts = None):
    return aodsfhInvocation(
        journal =      PVZD_SETTINGS['policyjournal'],
        poldirhtml =   PVZD_SETTINGS['poldirhtml'],
        poldirjson =   PVZD_SETTINGS['poldirjson'],
        shibacl =      PVZD_SETTINGS['shibacl'],
        trustedcerts = PVZD_SETTINGS['trustedcerts'],
    )

