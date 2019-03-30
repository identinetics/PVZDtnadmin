import logging
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
django.setup()

from PVZDpy.aodslisthandler import AodsListHandler
from PVZDpy.policychange import PolicyChangeIssuer, PolicyChangeNamespace, \
    PolicyChangeOrganization, PolicyChangeRevocation, PolicyChangeUserprivilege, \
    PolicyChangeList
from PVZDpy.policydict import OrgDict, PolicyDict
from fedop.models.issuer import Issuer
from fedop.models.revocation import Revocation
from fedop.models.namespace import Namespaceobj
from fedop.models.userprivilege import Userprivilege

from tnadmin.models.gvfederationorg import GvUserPortalOperator


class PolicyJournalUpdater():
    ''' Update policyjournal in 2 steps:
        (1) Collect changelist entries from the database and
        (2) append them to the policy journal
    '''
    def __init__(self):
        self.changelist = PolicyChangeList()
        self.policy_dict = PolicyDict()

    def append_poljournal(self) -> int:
        logging.debug('Records in changelist: ' + ', '.join([str(s) for s in self.changelist.changelist]))
        if len(self.changelist):
            aodslh = AodsListHandler()
            aodslh.append(self.changelist)
        return len(self.changelist)


    def get_changelist(self) -> PolicyChangeList:
        for policy_change_item in self._sync_gvuserportaloperator().changelist:
            self.changelist.append(policy_change_item)
        for policy_change_item in self._get_issuer_changes():
            self.changelist.append(policy_change_item)
        for policy_change_item in self._get_revocation_changes():
            self.changelist.append(policy_change_item)
        for policy_change_item in self._get_namespace_changes():
            self.changelist.append(policy_change_item)
        for policy_change_item in self._get_userprivilege_changes():
            self.changelist.append(policy_change_item)
        return self.changelist

    def _get_issuer_changes(self) -> list:
        i_list = []
        for i in Issuer.objects.filter(added_to_journal=False):
            irec_dict = PolicyChangeIssuer(
                i.subject_cn,
                i.pvprole,
                i.cacert,
                False)
            i_list.append(irec_dict)
        for i in Issuer.objects.filter(marked4delete=True, deleted_from_journal=False):
            irec_dict = PolicyChangeIssuer(
                i.subject_cn,
                i.pvprole,
                i.cacert,
                True)
            i_list.append(irec_dict)
        return i_list

    def _get_namespace_changes(self):
        n_list = []
        for n in Namespaceobj.objects.filter(added_to_journal=False):
            irec_dict = PolicyChangeNamespace(
                n.fqdn,
                n.gvouid_parent.gvouid.gvouid,
                False)
            n_list.append(irec_dict)
        for n in Namespaceobj.objects.filter(marked4delete=True, deleted_from_journal=False):
            irec_dict = PolicyChangeNamespace(
                n.fqdn,
                n.gvouid_parent.gvouid.gvouid,
                True)
            n_list.append(irec_dict)
        return n_list

    def _get_revocation_changes(self):
        r_list = []
        for r in Revocation.objects.filter(added_to_journal=False):
            irec_dict = PolicyChangeRevocation(
                r.cert,
                r.subject_cn,
                False)
            r_list.append(irec_dict)
        for r in Revocation.objects.filter(marked4delete=True, deleted_from_journal=False):
            irec_dict = PolicyChangeRevocation(
                r.cert,
                r.subject_cn,
                True)
            r_list.append(irec_dict)
        return r_list

    def _get_userprivilege_changes(self):
        u_list = []
        for u in Userprivilege.objects.filter(added_to_journal=False):
            inputrec_dict = PolicyChangeUserprivilege(
                '{cert}' + u.cert,
                u.gvouid_parent.gvouid.gvouid,
                u.subject_cn,
                False)
            u_list.append(inputrec_dict)
        for u in Userprivilege.objects.filter(marked4delete=True, deleted_from_journal=False):
            inputrec_dict = PolicyChangeUserprivilege(
                '{cert}' + u.cert,
                u.gvouid_parent.gvouid.gvouid,
                u.subject_cn,
                True)
            u_list.append(inputrec_dict)
        return u_list

    def _sync_gvuserportaloperator(self):
        ''' Policy journal mirrors a list of gvUserPortalOperator records.
            Get diff to keep the list in sync.
        '''
        tnadmin_orgdict = OrgDict()
        for o in GvUserPortalOperator.objects.all():
            tnadmin_orgdict.append(o.gvouid.gvouid, o.gvouid.cn)
        org_changelist = self.policy_dict.get_org_sync_changelist(tnadmin_orgdict)
        return org_changelist

if __name__ == '__main__':
    policy_journal_updater = PolicyJournalUpdater()
    count = len(policy_journal_updater.get_changelist())
    print(f"PolicyJournalUpdater::get_changelist: Appending {count} records in changelist")
    policy_journal_updater.append_poljournal()