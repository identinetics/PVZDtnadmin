import json
import logging
import os
import sys
import tempfile
from pathlib import Path

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
django.setup()

from PVZDpy.aodslisthandler import AodsListHandler
from PVZDpy.policychange import PolicyChangeIssuer, PolicyChangeNamespace, \
    PolicyChangeOrganization, PolicyChangeRevocation, PolicyChangeUserprivilege, \
    PolicyChangeList
from PVZDpy.policydict import OrgDict, PolicyDict
from fedop.models import *
from tnadmin.models.gvfederationorg import GvUserPortalOperator


class PolicyJournalUpdater():
    ''' Collect changelist entries from the database and append it to the policy journal '''
    def __init__(self):
        self.changelist = PolicyChangeList()
        self.policy_dict = PolicyDict()

    def load_changelist(self) -> None:
        self.build_changelist()
        if len(self.changelist):
            self.append_poljournal()
        # TODO: signal  "nothing to do"

    def build_changelist(self) -> None:
        for policy_change_item in self.sync_gvuserportaloperator().changelist:
            self.changelist.append(policy_change_item)
        for policy_change_item in self.get_issuer_changes():
            self.changelist.append(policy_change_item)
        for policy_change_item in self.get_revocation_changes():
            self.changelist.append(policy_change_item)
        for policy_change_item in self.get_namespace_changes():
            self.changelist.append(policy_change_item)
        for policy_change_item in self.get_userprivilege_changes():
            self.changelist.append(policy_change_item)

    # def _create_tempfile_from_str(self, contents: str) -> None:
    #    self.tmpfile = tempfile.NamedTemporaryFile(mode='w', prefix='pvzd_', suffix='.json', encoding='utf-8')
    #    self.tmpfile.write(contents)
    #    self.tmpfile.flush()

    # def _discard_tempfile(self) -> None:
    #    self.tmpfile.close()

    def get_issuer_changes(self) -> list:
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

    def get_namespace_changes(self):
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

    def get_revocation_changes(self):
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

    def get_userprivilege_changes(self):
        u_list = []
        for u in Userprivilege.objects.filter(added_to_journal=False):
            inputrec_dict = PolicyChangeUserprivilege(
                u.cert,
                u.gvouid_parent.gvouid.gvouid,
                u.subject_cn,
                False)
            u_list.append(inputrec_dict)
        for u in Userprivilege.objects.filter(marked4delete=True, deleted_from_journal=False):
            inputrec_dict = PolicyChangeUserprivilege(
                u.cert,
                u.gvouid_parent.gvouid.gvouid,
                u.subject_cn,
                True)
            u_list.append(inputrec_dict)
        return u_list

    def sync_gvuserportaloperator(self):
        ''' Policy journal mirrors a list of gvUserPortalOperator records.
            Get diff to keep the list in sync.
        '''
        tnadmin_orgdict = OrgDict()
        for o in GvUserPortalOperator.objects.all():
            tnadmin_orgdict.append(o.gvouid.gvouid, o.gvouid.cn)
        org_changelist = self.policy_dict.get_org_sync_changelist(tnadmin_orgdict)
        return org_changelist

    def append_poljournal(self):
        logging.debug('Records in changelist: ' + ', '.join([str(s) for s in self.changelist.changelist]))
        aodslh = AodsListHandler()
        aodslh.append(self.changelist)


if __name__ == '__main__':
    policy_journal_updater = PolicyJournalUpdater()
    policy_journal_updater.load_changelist()
