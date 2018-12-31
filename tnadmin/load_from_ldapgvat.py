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
from tnadmin.models import GvOrganisation as DbGvOrg
import tnadmin.models.gvOrg


def get_args():
    parser = argparse.ArgumentParser(description='Sync TNAdmin database with LdapGvAt')
    parser.add_argument('-c', '--max-inputrec', dest='max_input_rec', type=int, help='Do not read more than <value> records from ldap')
    parser.add_argument('-D', '--no-delete', dest='nodelete', action="store_true",
                        help='Do not delete records in database that are missing in ldap')
    parser.add_argument('-v', '--verbose', dest='verbose', action="store_true")
    return parser.parse_args()


def main():
    max_input_rec = 0
    for ldapOrg in LdapGvOrg.objects.all():
        try:
            dbOrg = DbGvOrg.objects.get(ldap_dn=ldapOrg.dn)
        except tnadmin.models.gvOrg.GvOrganisation.DoesNotExist:
            create_dbGvOrg_from_LdapGvOrg(ldapOrg)
        else:
            update_dbGvOrg_from_LdapGvOrg(dbOrg, ldapOrg)
        max_input_rec += 1
        if max_input_rec == args.max_input_rec:
            break


def create_dbGvOrg_from_LdapGvOrg(ldapOrg: LdapGvOrg):
    dbOrg = DbGvOrg()
    dbOrg.ldap_dn = ldapOrg.dn
    for attrib in DbGvOrg().defined_attr():
        source_attr = getattr(ldapOrg, attrib)
        setattr(dbOrg, attrib, source_attr)
    save_dbOrg(dbOrg, 'add')


def update_dbGvOrg_from_LdapGvOrg(dbOrg: DbGvOrg, ldapOrg: LdapGvOrg) -> bool:
    changed_attr = 0
    for attrib in DbGvOrg().defined_attr():
        source_attr = getattr(ldapOrg, attrib)
        if getattr(dbOrg, attrib) != source_attr:
            setattr(dbOrg, attrib, source_attr)
            changed_attr += 1
    if changed_attr > 0:
        save_dbOrg(dbOrg, 'update')
    else:
        if args.verbose: print(f'skipped {ldapOrg.dn}')


def save_dbOrg(dbOrg: DbGvOrg, op_message: str):
    try:
        dbOrg.save()
        if args.verbose: print(f'{op_message} {ldapGvOrg.dn}')
        return True
    except Exception as e:
        print(f'{op_message} {dvOrg.ldap_dn} failed with {str(e)}')
        return False


args = get_args()
main()
