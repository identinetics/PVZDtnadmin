import argparse
import os
import sys

import django
if __name__ == '__main__':
    django_proj_path = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(django_proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
    django.setup()
else:
    assert False
from ldapgvat.models import GvOrganisation as LdapGvOrg
import ldapgvat.models
from tnadmin.models import GvOrganisation as DbGvOrg
from tnadmin.models.get_defaults import get_default_org
from tnadmin.models.ldapsync import LdapSyncErrorPush, LdapSyncJobPush

class LdapSyncPush:
    def __init__(self):
        self.args = self.get_args()
        self.ldapSyncJob = LdapSyncJobPush()
        self.ldapSyncJob.save()
        self.dbgvat_entries = set()

    def get_args(self):
        parser = argparse.ArgumentParser(description='Sync TNAdmin database with LdapGvAt (upload to LDAP excluding AT:B:*)')
        parser.add_argument('-c', '--max-inputrec', dest='max_input_rec', type=int, default=0,
                            help='Do not read more than <value> records from ldap')
        parser.add_argument('-D', '--no-delete', dest='nodelete', action="store_true",
                            help='Do not delete records in ldap that are missing in db')
        parser.add_argument('-j', '--max-jobhistory', dest='max_jobhistory', type=int, default=10,
                            help='Keep max, <jobhistory> jobs, delete oldest first.')
        parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
        return parser.parse_args()

    def main(self):
        self.add_and_update()
        if not self.args.nodelete:
            self.delete_orphans()
        self.write_summary()
        self.ldapSyncJob_housekeeping()

    def add_and_update(self):
        max_input_rec = 0
        for dbOrg in DbGvOrg.objects.all().exclude(gvouid__startswith='AT:B:'):
            if self.is_fixed_record(dbOrg):
                continue
            self.ldapSyncJob.add_upd_db_records_read += 1
            create = False
            try:
                ldapOrg = LdapGvOrg.objects.get(dn=dbOrg.ldap_dn)
            except ldapgvat.models.GvOrganisation.DoesNotExist:
                create = True
            if create:
                self.create_LdapGvOrg_from_DbGvOrg(dbOrg)
            else:
                self.update_LdapGvOrg_from_DbGvOrg(dbOrg, ldapOrg)
            max_input_rec += 1
            if max_input_rec == self.args.max_input_rec and self.args.max_input_rec > 0:
                print(f'processing stopped after reading {max_input_rec} records from ldap.')
                break

    def delete_orphans(self):
        max_input_rec = 0
        for ldapOrg in LdapGvOrg.objects.all().exclude(gvouid__startswith='AT:B:'):
            self.ldapSyncJob.del_ldap_records_read += 1
            if ldapOrg.dn not in self.dbgvat_entries:
                self.del_ldapOrg(ldapOrg)
            max_input_rec += 1
            if max_input_rec == self.args.max_input_rec and self.args.max_input_rec > 0:
                print(f'processing stopped after reading {max_input_rec} records from db.')
                break

    def is_fixed_record(self, dbOrg: DbGvOrg) -> bool:
        return dbOrg.id == get_default_org() # AT:PVP:0 is hard coded, not synced to LDAP

    def ldapSyncJob_housekeeping(self):
        qs = LdapSyncJobPush.objects.order_by('-started_at')
        for i in range(self.args.max_jobhistory, len(qs)):
            ldapSyncJob = qs[i]
            if self.args.verbose: print(f'deleted LdapSyncJobPush {ldapSyncJob.id}')
            ldapSyncJob.delete()

    def write_summary(self):
        print(f'{self.ldapSyncJob.add_upd_db_records_read} db records read.')
        print(f'{self.ldapSyncJob.add_upd_records_skipped} db records skipped.')
        print(f'{self.ldapSyncJob.add_upd_records_added} records added to ldap.')
        print(f'{self.ldapSyncJob.add_upd_records_updated} records updated in ldap.')
        print(f'{self.ldapSyncJob.add_upd_records_update_failed} ldap updates failed.')
        print(f'{self.ldapSyncJob.del_ldap_records_read} ldap records read.')
        print(f'{self.ldapSyncJob.del_records_deleted } ldap records deleted.')
        print(f'{self.ldapSyncJob.del_records_delete_failed} ldap records delete failed.')
        self.ldapSyncJob.save()

    def create_LdapGvOrg_from_DbGvOrg(self, dbOrg: DbGvOrg):
        ldapOrg = LdapGvOrg()
        ldapOrg.dn = dbOrg.ldap_dn
        for attrib in DbGvOrg().defined_attr():
            source_val = getattr(dbOrg, attrib, None)
            setattr(ldapOrg, attrib, source_val)
        self.save_ldapOrg(ldapOrg, 'add')

    def update_LdapGvOrg_from_DbGvOrg(self, dbOrg: DbGvOrg, ldapOrg: LdapGvOrg):
        changed_attr = 0
        changed_attr_list = ''
        for attrib in DbGvOrg().defined_attr():
            source_val = getattr(dbOrg, attrib, None)
            dest_val = getattr(ldapOrg, attrib)
            if dest_val != source_val:
                setattr(ldapOrg, attrib, source_val)
                changed_attr += 1
                changed_attr_list += f'{attrib}: "{source_val}"/"{dest_val}", '
        if changed_attr > 0:
            if self.args.verbose: print(f'updating {ldapOrg.gvOuId} because of {changed_attr_list}')
            self.save_ldapOrg(ldapOrg, 'update')
        else:
            if self.args.verbose: print(f'skipped {dbOrg.ldap_dn}')
            self.ldapSyncJob.add_upd_records_skipped += 1

    def del_ldapOrg(self, ldapOrg: LdapGvOrg):
        try:
            ldapOrg.delete()
        except Exception as e:
            print(f'delete {ldapOrg.dn} failed with {str(e)}', file=sys.stderr)
            self.save_error_to_db('del', ldapOrg.dn, e)
            self.ldapSyncJob.del_records_delete_failed += 1
        else:
            self.ldapSyncJob.del_records_deleted += 1
            if self.args.verbose: print(f'{op_message} {ldapOrg.dn}')

    def save_ldapOrg(self, ldapOrg: LdapGvOrg, op_message: str):
        try:
            ldapOrg.save()
        except Exception as e:
            print(f'{op_message} {ldapOrg.dn} failed with {str(e)}', file=sys.stderr)
            self.save_error_to_db(op_message, ldapOrg.dn, e)
            self.ldapSyncJob.add_upd_records_update_failed += 1
        else:
            if op_message == 'add':
                self.ldapSyncJob.add_upd_records_added += 1
            else:
                self.ldapSyncJob.add_upd_records_updated += 1
            if self.args.verbose: print(f'{op_message} {dbOrg.ldap_dn}')

    def save_error_to_db(self, op_message, ldap_dn, e):
        ldapSyncError = LdapSyncErrorPush(
            op = op_message,
            ldap_dn = ldap_dn,
            message = str(e),
            job_id = self.ldapSyncJob
        )
        ldapSyncError.save()
        pass



if __name__ == '__main__':
    ldapSync = LdapSyncPush()
    ldapSync.main()
