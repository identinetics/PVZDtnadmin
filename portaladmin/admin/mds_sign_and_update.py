import json
from django.conf import settings
from django.contrib import messages
from ..constants import *
from ..exceptions import CancelRequest
from ..models import MDstatement
from PVZDpy.cresignedxml import creSignedXML
from PVZDpy.policystore import PolicyStore
from PVZDpy.samled_validator import SamlEdValidator
from PVZDpy.samlentitydescriptor import SAMLEntityDescriptorFromStrFactory

def mds_sign_and_update(_modeladmin, request, queryset,
                        used_uploaded_as_signed=False, unittest=True):
    mds = _get_selected_record_from_queryset(request, queryset, unittest)
    if used_uploaded_as_signed:
        mds.ed_signed = mds.ed_uploaded
    else:
        mds.ed_signed = _request_xmldsig(mds.ed_uploaded)
    mds.status = STATUS_SIGNATURE_APPLIED  # to be overwritten by revalidate
    _revalidate_after_signing(mds)
    mds.save(operation='mds_sign_and_update')

def get_selected_record_from_queryset(request, queryset, unittest) -> MDstatement:
    return _get_selected_record_from_queryset(request, queryset, unittest)

def _get_selected_record_from_queryset(request, queryset, unittest) -> MDstatement:
    if len(queryset.all()) > 1:
        _set_message_error(request, "Bitte genau einen EntityDescriptor auswählen", unittest)
    if len(queryset.all()) == 0:
        _set_message_error(request, "Kein EntityDescriptor ausgewählt/übergeben", unittest)
    this_rec = queryset.all()[0]
    if this_rec.status in (STATUS_REQUEST_QUEUE, STATUS_SIGNATURE_APPLIED, STATUS_ACCEPTED):
        _set_message_error(request, "EntityDescriptor wurde bereits signiert", unittest)
        raise CancelRequest
    if this_rec.status != STATUS_UPLOADED:
        _set_message_error(request, "Vor dem Signieren muss ein neuer Entityescriptor hochgeladen "
                                    "werden", unittest)
        raise CancelRequest
    if not this_rec.content_valid:
        _set_message_error(request, "Nur ein gültiger EntityDescriptor kann signiert werden",
                           unittest)
        raise CancelRequest
    return MDstatement.objects.get(pk=this_rec.pk)


def _request_xmldsig(ed_to_be_signed) -> str:
    ed = SAMLEntityDescriptorFromStrFactory(ed_to_be_signed)
    ed.remove_enveloped_signature()
    md_namespace_prefix = ed.get_namespace_prefix()
    return creSignedXML(ed.get_xml_str(),
                        sig_type='enveloped',
                        sig_position='/' + md_namespace_prefix + ':EntityDescriptor')


def _revalidate_after_signing(mds):
    policydir_fn = settings.PVZD_SETTINGS['policydir']
    with open(policydir_fn) as fd:
        policystore = PolicyStore(policydir=json.loads(fd.read()))
    ed_val = SamlEdValidator(policystore)
    ed_val.validate_entitydescriptor(ed_str_new=mds.ed_signed, sigval=True)
    mds.signer_subject = ed_val.signer_cert_cn
    if ed_val.authz_ok:
        mds.status = STATUS_REQUEST_QUEUE
        mds.signer_authorized = True
    else:
        mds.status = STATUS_REJECTED
        mds.signer_authorized = False
        mds.validation_message = json.dumps(ed_val.val_mesg_dict, indent=2)

def _set_message_error(request, msg, unittest=False):
    if unittest:
        raise UnittestException(msg)
    else:
        messages.error(request, msg)
