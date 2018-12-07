import json
import os.path
import sys
import django


if __name__ == '__main__':
    django_proj_path = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(django_proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
    django.setup()
else:
    assert False

from django.conf import settings
from PVZDpy.tests.common_fixtures import policydir1, policystore1
from fedop.models.issuer import *
from fedop.models.namespace import *
from fedop.models.revocation import *
from fedop.models.STPbetreiber import *

basedir = settings.BASE_DIR
#basedir = os.path.join('Users', 'admin', 'devl', 'python', 'identinetics', 'PVZDweb')


def main():
    add_stpbetreiber()
    add_namespaces()
    add_userprivileges()
    add_issuers()
    add_revocation()


def poldir1():
    fn = os.path.join(settings.BASE_DIR, 'PVZDlib', 'PVZDpy', 'tests', 'testdata', 'saml', 'poldir1.json')
    with open(fn) as fd:
        return json.loads(fd.read())


def add_stpbetreiber():
    org_recs = policystore1(poldir1()).get_all_orgids()
    for o in org_recs.keys():
        if not STPbetreiber.objects.filter(gvOuID__iexact=o):
            s = STPbetreiber()
            s.gvOuID = o
            s.cn = org_recs[o][0]
            s.save()
            print('added STPbetreiber %s' % s.gvOuID)
        else:
            print('skipped duplicate STPbetreiber entry %s' % o)


def add_namespaces():
    def _get_foreign_key(gvOuIdParent, ns_name) -> int:
        qs = STPbetreiber.objects.filter(gvOuID__iexact=gvOuIdParent)
        if len(qs) > 1:
            print('Importing namespace %s has more than one parent (org)' % ns_name)
            return None
        if not qs:
            print('Importing namespace %s: parent (org) not found' % ns_name)
            return None
        return qs[0]

    ns_recs = policystore1(poldir1()).get_registered_namespace_objs()
    for fqdn in ns_recs:
        ns_orgid = ns_recs[fqdn][0]
        parent_o = _get_foreign_key(ns_orgid, fqdn)
        if parent_o:
            ns = Namespaceobj(gvOuIdParent=parent_o, fqdn=fqdn)
            if not Namespaceobj.objects.filter(fqdn__iexact=fqdn):
                ns.save()
                print("added namespace %s" % fqdn)
            else:
                print("skipped duplicate namespace entry %s" % fqdn)


def add_userprivileges():
    def _get_foreign_key(gvOuIdParent, cert) -> int:
        qs = STPbetreiber.objects.filter(gvOuID__iexact=gvOuIdParent)
        if len(qs) > 1:
            print('Importing userprivilege %s has more than one parent (org)' % cert)
            return None
        if not qs:
            print('Importing userprivilege %s: parent (org) not found' % cert)
            return None
        return qs[0]

    u_recs = policystore1(poldir1()).get_userprivileges()
    for cert in u_recs:
        u_orgid = u_recs[cert][0]
        parent_o = _get_foreign_key(u_orgid, cert)
        if parent_o:
            u = Userprivilege(gvOuIdParent=parent_o, cert=cert)
            if not Userprivilege.objects.filter(cert=cert):  # assume base64 without whitespace
                u.save()
                print("added userprivilege %s" % cert)
            else:
                print("skipped duplicate userprivilege entry %s" % cert)


def add_issuers():
    i_recs = policystore1(poldir1()).get_issuers()
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
    r_recs = policystore1(poldir1()).get_revoked_certs()
    for cert in r_recs:
        if not Revocation.objects.filter(cert=cert):
            r = Revocation(cert=cert)
            r.save()
            print('added revocation_cert %s' % cert)
        else:
            print('skipped duplicate revocation_cert %s' % cert)



main()



