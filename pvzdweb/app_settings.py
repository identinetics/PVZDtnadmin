from django.conf import settings
from PVZDpy.invocation.aodsfhinvocation import AodsfhInvocation
from PVZDpy.invocation.aodslhinvocation import AodslhInvocation


def get_aodsfhInvocation():
    return AodsfhInvocation(
        settings.PVZD_SETTINGS['policyjournal'],
        settings.PVZD_SETTINGS['trustedcerts']
    )


def get_aodslhInvocation():
    return AodslhInvocation(
        poldirhtml =   settings.PVZD_SETTINGS['poldirhtml'],
        poldirjson =   settings.PVZD_SETTINGS['poldirjson'],
        shibacl =      settings.PVZD_SETTINGS['shibacl'],
    )

