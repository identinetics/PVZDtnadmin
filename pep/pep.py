import logging
import os
import sys
import django
if __name__ == '__main__':
    django_proj_path = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(django_proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
    django.setup()
from django.conf import settings
from PVZDpy.constants import *
from PVZDpy.samled_validator import SamlEdValidator
from PVZDpy.userexceptions import *
from portaladmin.models import MDstatement
from portaladmin.constants import STATUS_REQUEST_QUEUE, STATUS_REJECTED, STATUS_ACCEPTED

from get_pep_logger import get_pep_logger
from get_policystore import get_policystore


__author__ = 'r2h2'


class PEP:
    """ The PEP (Policy Enforcement Point) performs for each invocation:

        for each MDstatement with status = request_queue
            if it conforms to the policy
                set status to "accepted"
                publish/unpublish the EntityDescriptor
            else
                set the status to "rejected"
    """
    def __init__(self):
        self.logger = get_pep_logger()
        self.logfilepep = settings.PVZD_SETTINGS['logfilepep']
        self.loglevelpep = settings.PVZD_SETTINGS['loglevelpep']
        self.pepoutdir = settings.PVZD_SETTINGS['pepoutdir']
        self.regauthority = settings.PVZD_SETTINGS['regauthority']
        self.ed_val = SamlEdValidator(get_policystore(debug_speedup=True))  # TODO: False for qa+prod

    def _update_pepout(self, mds):
        ed = mds.ed_val.ed
        fn = os.path.join(self.pepoutdir, ed.get_filename_from_entityid())
        if request.is_delete():
            os.unlink(fn)  # TODO: save logging, handle exceptions
            logging.info('Entity {} unpublished'.format(entityid))
        else:
            ed.remove_enveloped_signature()
            ed.set_registrationinfo(self.regauthority)
            ed.write(new_filename=fn)
            logging.info('Entity {} published'.format(entityid))

    def process_new_input(self):
        count_accepted = 0
        count_rejected = 0
        for mds_rec in MDstatement.objects.filter(status=STATUS_REQUEST_QUEUE):
            mds = MDstatement.objects.get(pk=mds_rec.pk)
            mds.validate()
            if mds.content_valid and mds.signer_authorized:
                mds.status = STATUS_ACCEPTED
                mds.save()
                self._update_pepout(mds)
                count_accepted += 1
            else:
                mds.status = STATUS_REJECTED
                mds.save()
                count_rejected += 1
                logging.info('Metadata Statement {} rejected'.format(entityid))
        logging.debug('accepted: {}, rejected: {}')


if __name__ == '__main__':
    pep = PEP()
    pep.process_new_input()
else:
    assert False
