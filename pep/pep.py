import logging
import os
import re
import sys
import tempfile
from PVZDpy.constants import *
from PVZDpy.invocation.abstractinvocation import AbstractInvocation
from PVZDpy.policydict import get_policy_dict
from PVZDpy.samled_validator import SamlEdValidator
from PVZDpy.userexceptions import *
from pvzdweb.app_settings import get_aodslhInvocation
from portaladmin.models import MDstatement
from .loggingconfig import LoggingConfig


__author__ = 'r2h2'


""" The PEP (Policy Enforcement Point) performs for each invocation:

    for each MDstatement with status = request_queue
        check if it conforms to the policy
        if it is OK
            set status to "accepted"
            publish/unpublish the EntityDescriptor
        else
            set the status to "rejected"
"""

request_counter = 0
request_counter_accepted = 0
request_counter_rejected = 0
try:
    policyDict = get_policy_dict(get_aodslhInvocation()))
    ed_validator = SamlEdValidator(policyDict)
except Exception as e:
    logging.log(LOGLEVELS['CRITICAL'], str(e) + '\nterminating PEP.')
    raise


def _update_mds_status(pk, entityid, status):
    MDstatement.objects.filter(pk=pk).update(status=status)
    logging.info('request for {} {}'.format(entityid, status))


def _update_pepout(request):
    fn = SAMLEntityDescriptor.get_filename_from_entityid(request.get_entityID())
    if request.is_delete():

        unlink

def pep(testrunnerInvocation=None):
    if testrunnerInvocation:
        # CLI args and logger set by unit test
        invocation = testrunnerInvocation
        exception_lvl = LOGLEVELS['DEBUG']
    else:
        invocation = CliPep()
        logbasename = re.sub(r'\.py$', '', os.path.basename(__file__))
        logging_config = LoggingConfig(logbasename,
                                       console=True,
                                       console_level=invocation.args.loglevel,
                                       file_level=invocation.args.loglevel)
        exception_lvl = LOGLEVELS['ERROR']
        #logging.debug('logging level=' + LOGLEVELS_BY_INT[invocation.args.loglevel])

    for request in MDstatement.objects.filter(status='request_queue'):
        ed_validator.validate_entitydescriptor(ed_str_new=request.ed_signed)
        if ed_validator.content_val_ok and ed_validator.authz_ok:
            _update_mds_status(request_pk, request.get_entityID(), STATUS_ACCEPTED)
            _update_pepout(request)
        else:
            _update_mds_status(request_pk, request.get_entityID(), STATUS_REJECTED)

    if pep.request_counter == 0 or testrunnerInvocation:
        summary_loglevel = LOGLEVELS['DEBUG']
    else:
        summary_loglevel = LOGLEVELS['INFO']
    logging.log(summary_loglevel, 'files in request queue processed: ' + str(pep.request_counter) + \
                '; accepted: ' + str(pep.request_counter_accepted) + \
                '; rejected: ' + str(pep.request_counter_rejected) + '.')


if __name__ == '__main__':
    if sys.version_info < (3, 4):
        raise "must use python 3.4 or higher"
    pep()
