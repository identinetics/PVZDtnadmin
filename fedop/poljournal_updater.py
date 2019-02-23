import json
import logging
import os
import sys
import tempfile
from pathlib import Path

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
django.setup()

from PVZDpy.aodsfilehandler import AODSFileHandler
from PVZDpy.aodslisthandler import AodsListHandler
from PVZDpy.PolicyChange import AodsChangeList, PolicyChangeIssuer, PolicyChangeNamespace, \
    PolicyChangeOrganization, PolicyChangeRevocation, PolicyChangeUserprivilege
from fedop.config.get_policystore import get_policystore
from fedop.models import *
from pvzdweb.app_settings import get_aodsfhInvocation, get_aodslhInvocation
from tnadmin.models.gvfederationorg import GvUserPortalOperator


class PolicyJournalUpdater():
    def __init__(self):
        self.changelist = PolicyChangeList()
        self.policy_store = get_policystore()

    def main(self):
        self.build_changelist()
        if len(self.changelist):
            self.append_poljournal()
        # TODO: signal  "nothing to do"

    def build_changelist(self):
        self.changelist.append(self.sync_gvuserportaloperator())
        self.changelist.append(self.get_issuer_changes())
        self.changelist.append(self.get_revocation_changes())
        self.changelist.append(self.get_namespace_changes())
        self.changelist.append(self.get_userprivilege_changes())
        changelist_json = json.dumps(self.changelist)
        self._create_tempfile_from_str(changelist_json )

    def append_poljournal(self):
        logging.debug('Records in changelist: ' + ', '.join([str(s) for s in self.changelist]))
        aods_fh = AODSFileHandler(get_aodsfhInvocation())
        aodslh_inv = get_aodslhInvocation()
        aodslh_inv.inputfilename = self.tmpfile.name
        aods_lh = AodsListHandler(aods_fh, aodslh_inv)
        aods_lh.aods_append()
        self.refresh_policy_store_cache()
        self._discard_tempfile()

    def _create_tempfile_from_str(self, contents: str):
        self.tmpfile = tempfile.NamedTemporaryFile(mode='w', prefix='pvzd_', suffix='.json', encoding='utf-8')
        self.tmpfile.write(contents)
        self.tmpfile.flush()

    def _discard_tempfile(self):
        self.tmpfile.close()

    def get_issuer_changes(self):
        i_list = []
        for i in Issuer.objects.filter(added_to_journal=False):
            irec_dict = PolicyChangeIssuer(
                i.subject_cn,
                i.pvprole,
                i.cacert,
                False).inputrec
            i_list.append(irec_dict)
        for i in Issuer.objects.filter(marked4delete=True, deleted_from_journal=False):
            irec_dict = PolicyChangeIssuer(
                i.subject_cn,
                i.pvprole,
                i.cacert,
                True).inputrec
            i_list.append(irec_dict)
        return i_list

    def get_namespace_changes(self):
        n_list = []
        for n in Namespaceobj.objects.filter(added_to_journal=False):
            irec_dict = PolicyChangeNamespace(
                n.fqdn,
                n.gvouid_parent.gvouid.gvouid,
                False).inputrec
            n_list.append(irec_dict)
        for n in Namespaceobj.objects.filter(marked4delete=True, deleted_from_journal=False):
            irec_dict = PolicyChangeNamespace(
                n.fqdn,
                n.gvouid_parent.gvouid.gvouid,
                True).inputrec
            n_list.append(irec_dict)
        return n_list

    def get_revocation_changes(self):
        r_list = []
        for r in Revocation.objects.filter(added_to_journal=False):
            irec_dict = PolicyChangeRevocation(
                r.cert,
                r.subject_cn,
                False).inputrec
            r_list.append(irec_dict)
        for r in Revocation.objects.filter(marked4delete=True, deleted_from_journal=False):
            irec_dict = PolicyChangeRevocation(
                r.cert,
                r.subject_cn,
                True).inputrec
            r_list.append(irec_dict)
        return r_list

    def get_userprivilege_changes(self):
        u_list = []
        for u in Userprivilege.objects.filter(added_to_journal=False):
            inputrec_dict = PolicyChangeUserprivilege(
                u.cert,
                u.gvouid_parent.gvouid.gvouid,
                u.subject_cn,
                False).inputrec
            u_list.append(inputrec_dict)
        for u in Userprivilege.objects.filter(marked4delete=True, deleted_from_journal=False):
            inputrec_dict = PolicyChangeUserprivilege(
                u.cert,
                u.gvouid_parent.gvouid.gvouid,
                u.subject_cn,
                True).inputrec
            u_list.append(inputrec_dict)
        return u_list

    def sync_gvuserportaloperator(self):
        ''' Policy journal mirrors a list of gvUserPortalOperator records.
            Get diff to keep the list in sync.
        '''
        def get_inputrec(gvouid, cn, delete=None) -> dict:
            return PolicyChangeOrganization(gvouid, cn, delete).inputrec

        def add_missing_items():
            for gvouid in gvouids_in_db.keys():
                if gvouid not in gvouids_in_pj:
                    cn = gvouids_in_db[gvouid]
                    o_list.append(get_inputrec(gvouid, cn, delete=False))

        def delete_orphans():
            for gvouid in gvouids_in_pj:
                if gvouid not in gvouids_in_db.keys():
                    cn = self.policy_store.get_orgcn(gvouid)
                    o_list.append(get_inputrec(gvouid, cn, delete=True))

        o_list = []
        gvouids_in_pj = set(self.policy_store.get_all_orgids().keys())
        gvouids_in_db = {}
        for o in GvUserPortalOperator.objects.all():
            gvouids_in_db[o.gvouid.gvouid] = o.gvouid.cn
        add_missing_items()
        delete_orphans()
        return o_list

    def refresh_policy_store_cache(self):
        _ = get_policystore()   # get_policystore will copy it form the db


if __name__ == '__main__':
    policy_journal_updater = PolicyJournalUpdater()
    policy_journal_updater.main()
