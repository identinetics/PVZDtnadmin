import datetime
import json
import pathlib
import os
import sys

import django

if __name__ != '__main__':
    sys.exit(1)

projhome = pathlib.Path('sys.argv[0]').parent.parent.parent
sys.path.append(projhome)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
django.setup()

#from ldapgvat.models import GvUserPortal as LdapUserPortal
import ldapgvat.models
from tnadmin.models.constants import *
from tnadmin.models.gvfederationorg import *
from tnadmin.models.gvorg import *
import tnadmin.models.gvorg

class InitialLoadFedOrg:
    def main(self):
        self.exit_code = 0
        self.load_PVV_org()
        self.load_STP_DL_org()
        self.load_PV_ZUGRIFF_org()
        sys.exit(self.exit_code)

    def load_PVV_org(self):
        fedorg_pvv = pathlib.Path(sys.argv[0]).parent / 'tests' / 'data' / 'fedorg_pvv.json'
        print(f'loading FederationOrg/PVV from {fedorg_pvv}')
        with fedorg_pvv.open() as fd:
            org_pvv = json.load(fd)
            for vkz in org_pvv:
                gvorg = self.get_gvorg_by_vkz(vkz)
                if gvorg:
                    fedorg = GvFederationOrg(gvouid=gvorg)
                    fedorg.gvContractStatus = LEGAL_BASIS_PVV
                    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
                    fedorg.save()

    def load_STP_DL_org(self):
        fedorg_stp_dl = pathlib.Path(sys.argv[0]).parent / 'tests' / 'data' / 'fedorg_stp_dl.json'
        print(f'loading FederationOrg/STP-DL from {fedorg_stp_dl}')
        with fedorg_stp_dl.open() as fd:
            org_stp_dl = json.load(fd)
            for (ouid, cn) in org_stp_dl.items():
                gvorg = self.get_gvorg_by_ouid(ouid, cn)
                if gvorg:
                    fedorg = GvFederationOrg(gvouid=gvorg)
                    fedorg.gvContractStatus = LEGAL_BASIS_PROCESSOR_IDP
                    fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
                    fedorg.save()

    def load_PV_ZUGRIFF_org(self):
        for userportal in ldapgvat.models.GvUserPortal.objects.all():
            if 'gvuserportal' in [oc.lower() for oc in userportal.object_classes] and \
                userportal.gvParticipants:
                print('found {ldaporg} with {len(userportal.gvParticipants)} participants')
                for ouid in userportal.gvParticipants:
                    gvorg = self.get_gvorg_by_ouid(ouid, '')
                    if gvorg:
                        fedorg = GvFederationOrg(gvouid=gvorg)
                        fedorg.gvContractStatus = LEGAL_BASIS_ENTITLED_ORG
                        fedorg.gvSource = str(datetime.datetime.now()) + ' initial_load_fedorg'
                        fedorg.save()
                    else:
                        print(f'participant {ouid} registered in {userportal.dn} not found in gvOrganisation')

    def get_gvorg_by_ouid(self, ouid: str, cn: str) -> GvOrganisation:
        try:
            gvorg = GvOrganisation.objects.get(gvOuId=ouid)
            return gvorg
        except tnadmin.models.gvorg.GvOrganisation.DoesNotExist:
            print(f"gvOrganisation '{cn}' not found via gvOuId='{ouid}'", file=sys.stderr)
            self.exit_code = 1
            return None


    def get_gvorg_by_vkz(self, vkz: str) -> GvOrganisation:
        try:
            gvorg = GvOrganisation.objects.get(gvOuVKZ=vkz)
            return gvorg
        except tnadmin.models.gvorg.GvOrganisation.DoesNotExist:
            print(f"gvOrganisation not found via gvOuVKZ='{vkz}'", file=sys.stderr)
            self.exit_code = 1
        return None


    def map_gvorg_to_fedorg_legal_basis(self, gvorg: GvOrganisation):
        if re.search(r'^L\d$', gvOuVKZ):
            return LEGAL_BASIS_PVV
        if re.search(r'^B[A-Za-z]', gvOuVKZ):
            if gvOuVKZ != 'BPDION':
                return LEGAL_BASIS_PVV
        if gvOuVKZ in ('BBA-STA', ):
                return LEGAL_BASIS_PVV


InitialLoadFedOrg().main()
