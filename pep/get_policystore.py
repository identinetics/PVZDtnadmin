import json
from django.conf import settings
from PVZDpy.policystore import PolicyStore
from pvzdweb.app_settings import get_aodslhInvocation

def get_policystore(debug_speedup=False):
    if debug_speedup:
        policydir_fn = settings.PVZD_SETTINGS['policydir']
        with open(policydir_fn) as fd:
            return PolicyStore(policydir=json.loads(fd.read()))
    else:
        try:
            return PolicyStore(get_aodslhInvocation())
        except Exception as e:
            logging.log(LOGLEVELS['CRITICAL'], str(e) + '\nterminating PEP.')
            raise
