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
from django.core.exceptions import ObjectDoesNotExist
from ldapgvat.models import GvOrganisation as LdapGvOrg
from tnadmin.models import GvOrganisation as DbGvOrg
from tnadmin.models.ldapsync import LdapSyncError, LdapSyncJob
import tnadmin.models.gvorg

class LdapSync:
    def __init__(self):
        self.args = self.get_args()
        self.ldapSyncJob = LdapSyncJob()
        self.ldapSyncJob.save()

    def get_args(self):
        parser = argparse.ArgumentParser(description='Sync TNAdmin database with LdapGvAt')
        parser.add_argument('-c', '--max-inputrec', dest='max_input_rec', type=int, default=0,
                            help='Do not read more than <value> records from ldap')
        parser.add_argument('-D', '--no-delete', dest='nodelete', action="store_true",
                            help='Do not delete records in database that are missing in ldap')
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
        for ldapOrg in LdapGvOrg.objects.all():
            self.ldapSyncJob.add_upd_ldap_records_read += 1
            #if ldapOrg.gvOuId in ('AT:L6', 'AT:VKZ:XFN-295183v', 'AT:VKZ:UFB-262918w', 'AT:VKZ:XFN-213441i', 'AT:VKZ:XFN-160573m'):
            #    print(f'debug: missing {ldapOrg.gvOuId}?')
            create = False
            try:
                dbOrg = DbGvOrg.objects.get(ldap_dn=ldapOrg.dn)
            except tnadmin.models.gvorg.GvOrganisation.DoesNotExist:
                create = True
            if create:
                self.create_dbGvOrg_from_LdapGvOrg(ldapOrg)
            else:
                self.update_dbGvOrg_from_LdapGvOrg(dbOrg, ldapOrg)
            max_input_rec += 1
            if max_input_rec == self.args.max_input_rec and self.args.max_input_rec > 0:
                print(f'processing stopped after reading {max_input_rec} records from ldap.')
                break

    def delete_orphans(self):
        max_input_rec = 0
        for dbOrg in DbGvOrg.objects.all():
            self.ldapSyncJob.del_db_records_read += 1
            try:
                dbOrg = DbGvOrg.objects.get(dn=dbOrg.ldap_dn)
            except tnadmin.models.gvorg.GvOrganisation.DoesNotExist:
                self.create_dbGvOrg_from_LdapGvOrg(ldapOrg)
            else:
                self.update_dbGvOrg_from_LdapGvOrg(dbOrg, ldapOrg)
            max_input_rec += 1
            if max_input_rec == self.args.max_input_rec and self.args.max_input_rec > 0:
                print(f'processing stopped after reading {max_input_rec} records from db.')
                break

    def ldapSyncJob_housekeeping(self):
        qs = LdapSyncJob.objects.order_by('-started_at')
        for i in range(self.args.max_jobhistory, len(qs)):
            ldapSyncJob = qs[i]
            if self.args.verbose: print(f'deleted LdapSyncJob {ldapSyncJob.id}')
            ldapSyncJob.delete()


    def write_summary(self):
        print(f'{self.ldapSyncJob.add_upd_ldap_records_read} ldap records read.')
        print(f'{self.ldapSyncJob.add_upd_records_skipped} ldap records skipped.')
        print(f'{self.ldapSyncJob.add_upd_records_added} ldap records added to db.')
        print(f'{self.ldapSyncJob.add_upd_records_updated} ldap records updated in db.')
        print(f'{self.ldapSyncJob.add_upd_records_update_failed} db updates failed.')
        print(f'{self.ldapSyncJob.del_db_records_read} db records read.')
        print(f'{self.ldapSyncJob.del_records_deleted } db records deleted.')
        print(f'{self.ldapSyncJob.del_records_delete_failed} db records delete failed.')
        self.ldapSyncJob.save()

    def create_dbGvOrg_from_LdapGvOrg(self, ldapOrg: LdapGvOrg):
        dbOrg = DbGvOrg()
        dbOrg.ldap_dn = ldapOrg.dn
        for attrib in DbGvOrg().defined_attr():
            source_attr = getattr(ldapOrg, attrib, None)
            setattr(dbOrg, attrib, source_attr)
        self.save_dbOrg(dbOrg, 'add')

    def update_dbGvOrg_from_LdapGvOrg(self, dbOrg: DbGvOrg, ldapOrg: LdapGvOrg):
        changed_attr = 0
        changed_attr_list = ''
        for attrib in DbGvOrg().defined_attr():
            source_val = getattr(ldapOrg, attrib, None)
            dest_val = getattr(dbOrg, attrib)
            if dest_val != source_val:
                setattr(dbOrg, attrib, source_val)
                changed_attr += 1
                changed_attr_list += f'{attrib}: "{source_val}"/"{dest_val}", '
        if changed_attr > 0:
            print(f'debug: updating {ldapOrg.gvOuId} because of {changed_attr_list}')
            self.save_dbOrg(dbOrg, 'update')
        else:
            if self.args.verbose: print(f'skipped {ldapOrg.dn}')
            self.ldapSyncJob.add_upd_records_skipped += 1

    def del_dbOrg(self, dbOrg: DbGvOrg):
        try:
            dbOrg.delete()
        except Exception as e:
            print(f'delete {dbOrg.ldap_dn} failed with {str(e)}', file=sys.stderr)
            self.save_error_to_db('del', dbOrg.ldap_dn, e)
            self.ldapSyncJob.del_records_delete_failed += 1
        else:
            self.ldapSyncJob.del_records_deleted += 1
            if self.args.verbose: print(f'{op_message} {dbOrg.ldap_dn}')

    def save_dbOrg(self, dbOrg: DbGvOrg, op_message: str):
        try:
            dbOrg.save()
        except Exception as e:
            print(f'{op_message} {dbOrg.ldap_dn} failed with {str(e)}', file=sys.stderr)
            self.save_error_to_db(op_message, dbOrg.ldap_dn, e)
            self.ldapSyncJob.add_upd_records_update_failed += 1
        else:
            if op_message == 'add':
                self.ldapSyncJob.add_upd_records_added += 1
            else:
                self.ldapSyncJob.add_upd_records_updated += 1
            if self.args.verbose: print(f'{op_message} {dbOrg.ldap_dn}')

    def save_error_to_db(self, op_message, ldap_dn, e):
        ldapSyncError = LdapSyncError(
            op = op_message,
            ldap_dn = ldap_dn,
            message = str(e),
            job_id = self.ldapSyncJob
        )
        ldapSyncError.save()
        pass



if __name__ == '__main__':
    ldapSync = LdapSync()
    ldapSync.main()
