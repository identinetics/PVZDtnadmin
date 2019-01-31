import json
from pathlib import Path
from django.conf import settings
from PVZDpy.policy_journal import PolicyJournal
from pvzdweb.app_settings import get_aodslhInvocation

''' The primary location of the PolicyJournal is the database table fedop_policy_journal.
    It is copied to the file system, as the PVZDpy classes expect it there. 
'''

def get_policystore(debug_speedup=False) -> PolicyStore:
    if debug_speedup:
        policydir_fn = settings.PVZD_SETTINGS['policydir']
        with open(policydir_fn) as fd:
            return PolicyStore(policydir=json.loads(fd.read()))
    else:
        try:
            _copy_file_from_db()
            return PolicyStore(get_aodslhInvocation())
        except Exception as e:
            logging.log(LOGLEVELS['CRITICAL'], str(e) + '\nterminating PEP.')
            raise

def _copy_file_from_db():
    pj = PolicyJournal.objects.all()[0]
    policyjournal_path = Path(settings.PVZD_SETTINGS['policyjournal'])
    with policyjournal_path.open(mode='w') as fd:
        fd.write(pj.policy_journal)