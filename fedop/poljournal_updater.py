from pathlib import Path

import django
projhome = Path('sys.argv[0]').parent.parent.parent
sys.path.append(projhome)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
django.setup()

from PVZDpy.aodsfilehandler import AODSFileHandler
from PVZDpy.aodslisthandler import AodsListHandler
from PVZDpy.inputrecord import InputRecordIssuer, InputRecordNamespace, InputRecordRevocation, InputRecordUserprivilege
from common import get_policystore
from fedop.models.issuer import *
from fedop.models.revocation import *
from fedop.models.namespace import *
from fedop.models.policy_journal import *
from fedop.models.userprivilege import *
from pvzdweb.app_settings import get_aodslhInvocation
from tnadmin.models.gvfederationorg import GvUserPortalOperator


class PolicyJournalUpdater():
    def __init__(self):
        self.changelist = []

    def main(self):
        self.build_changelist()
        #policy_store = self.get_policystore()
        #aods_fh = AODSFileHandler(get_aodslhInvocation())
        #aods_lh = AodsListHandler(aodsFileHandlder, get_aodslhInvocation())
        #self.refresh_policy_store_cache()

    def build_changelist(self):
        self.changelist.append(self.get_issuer_changes())
        #self.changelist.append(self.get_revocation_changes())
        #self.changelist.append(self.get_namespace_changes())
        #self.changelist.append(self.get_userprivilege_changes())

    def get_issuer_changes(self, load_fedop1):
        i_list = []
        for i in Issuer.objects.filter(added_to_journal=False):
            i_list.append(InputRecordIssuer(
                i.subject_cn,
                i.pvprole,
                i.cert
                False
            ))
        for i in Issuer.objects.filter(marked4delete=True, deleted_from_journal=False):
            i_list.append(InputRecordIssuer(
                i.subject_cn,
                i.pvprole,
                i.cert
                True
            ))

    def get_revocation_changes(self):
        r = Revocation.objects.all()[0]  # only one item in testdata

    def get_namespace_changes(self):
        i = Namespaceobj()

    def get_userprivilege_changes(self):
        u = Userprivilege(cert=cert)

    def refresh_policy_store_cache(self):
        _ = get_policystore()   # get_policystore will copy it form the db


if __name__ == '__main__':
    policy_journal_updater = PolicyJournalUpdater()
    policy_journal_updater.main()
else:
    sys.exit(1)