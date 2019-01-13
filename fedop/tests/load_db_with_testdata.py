import json
import os.path
from pathlib import Path
import sys
import django


if __name__ == '__main__':
    #django_proj_path = os.path.dirname(os.path.dirname(os.getcwd()))
    #sys.path.append(django_proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings_allapps")
    print(os.environ["DJANGO_SETTINGS_MODULE"])
    django.setup()
else:
    assert False

from django.conf import settings
from fedop.models.issuer import Issuer
from fedop.models.namespace import Namespaceobj
from fedop.models.revocation import Revocation
from fedop.models.userprivilege import Userprivilege
from PVZDpy.policystore import PolicyStore
from tnadmin.models.gvfederationorg import GvUserPortalOperator
from tnadmin.models.gvorg import GvOrganisation

basedir = settings.BASE_DIR
testdata_dir = Path(basedir) / 'fedop' / 'tests' / 'data'


def main():
    add_namespaces()
    add_userprivileges()
    add_issuers()
    add_revocation()


def policystore3():
    p = Path(testdata_dir) / 'poldir3.json'
    with p.open() as fd:
        policydir1 = json.load(fd)
    return PolicyStore(policydir=policydir1)


def add_namespaces():
    def _get_foreign_key_parent_obj(gvouid_parent, ns_name) -> int:
        try:
            o = GvOrganisation.objects.get(gvouid=gvouid_parent)
        except GvOrganisation.DoesNotExist:
            print(f'Importing {ns_name}: {gvouid_parent} not a registered organisation')
            return None
        qs = GvUserPortalOperator.objects.filter(gvouid_id=o.id)
        if len(qs) > 1:
            print('Importing namespace %s has more than one parent (org)' % ns_name)
            return None
        if not qs:
            print('Importing namespace %s: parent (org) not a UserPortalOperator' % ns_name)
            return None
        return qs[0]

    ns_recs = policystore3().get_registered_namespace_objs()
    for fqdn in ns_recs:
        ns_orgid = ns_recs[fqdn][0]
        parent_o = _get_foreign_key_parent_obj(ns_orgid, fqdn)
        if parent_o:
            ns = Namespaceobj(gvouid_parent=parent_o, fqdn=fqdn)
            if not Namespaceobj.objects.filter(fqdn__iexact=fqdn):
                ns.save()
                print("added namespace %s" % fqdn)
            else:
                print("skipped duplicate namespace entry %s" % fqdn)


def add_userprivileges():
    def _get_foreign_key_parent_obj(gvouid_parent, cert) -> int:
        qs = GvUserPortalOperator.objects.filter(gvouid__gvouid=gvouid_parent)
        if len(qs) > 1:
            print('Importing userprivilege %s has more than one parent (org)' % cert)
            return None
        if not qs:
            print('Importing userprivilege %s: parent (org) not found' % cert)
            return None
        return qs[0]

    u_recs = policystore3().get_userprivileges()
    for cert in u_recs:
        u_orgid = u_recs[cert][0]
        u_username = u_recs[cert][1]
        parent_o = _get_foreign_key_parent_obj(u_orgid, cert)
        if parent_o:
            u = Userprivilege(gvouid_parent=parent_o, cert=cert)
            if not Userprivilege.objects.filter(cert=cert):  # assume base64 without whitespace
                u.save()
                print(f"added userprivilege for {u_username} ({u_orgid})")
            else:
                print(f"skipped duplicate userprivilege entry for {u_username} ({u_orgid}")


def add_issuers():
    i_recs = policystore3().get_issuers()
    for subject_cn in i_recs.keys():
        if not Issuer.objects.filter(subject_cn=subject_cn):
            i = Issuer(subject_cn=subject_cn)
            i.pvprole = i_recs[subject_cn][0]
            i.cacert = i_recs[subject_cn][1]
            i.save()
            print('added Issuer %s' % subject_cn)
        else:
            print('skipped duplicate Issuer entry %s' % subject_cn)


def add_revocation():
    r_recs = policystore3().get_revoked_certs()
    for cert in r_recs:
        # if not Revocation.objects.filter(cert=cert):   # TODO: compare only public key
        #     r = Revocation(cert=cert)
        #     r.save()
        #     print('added revocation_cert %s' % cert)
        # else:
        #     print('skipped duplicate revocation_cert %s' % cert)
        rec_found = False
        try:
            Revocation.objects.get(cert=cert)
            rec_found = True
            print('skipped duplicate revocation_cert %s' % cert)
        except Revocation.DoesNotExist:
            pass
        if not rec_found:
            r = Revocation(cert=cert)
            r.save()
            print('added revocation_cert %s' % cert)


main()
