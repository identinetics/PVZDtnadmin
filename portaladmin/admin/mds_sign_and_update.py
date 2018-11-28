from django.contrib import messages
from ..constants import *
from ..models import MDstatement
from PVZDpy.cresignedxml import creSignedXML
from PVZDpy.samled_validator import SamlEdValidator
from PVZDpy.samlentitydescriptor import SAMLEntityDescriptorFromStrFactory


def mds_sign_and_update(_modeladmin, request, queryset):
    mds = _get_selected_record_from_queryset()
    mds.ed_signed = _request_xmldsig(mds.ed_uploaded)
    self.status = STATUS_SIGNATURE_APPLIED  # to be overwritten by revalidate
    _revalidate_after_signing()
    mds.save()


def _get_selected_record_from_queryset() -> MDstatement:
    if len(queryset.all()) > 1:
        messages.error(request, "Bitte genau einen EntityDescriptor auswählen")
    this_rec = queryset.all()[0]
    return MDstatement.objects.get(pk=this_rec.pk)


def _request_xmldsig(ed_to_be_signed) -> str:
    ed = SAMLEntityDescriptorFromStrFactory(ed_to_be_signed)
    ed.remove_enveloped_signature()
    md_namespace_prefix = ed.get_namespace_prefix()
    return creSignedXML(ed.get_xml_str(),
                        sig_type='enveloped',
                        sig_position='/' + md_namespace_prefix + ':EntityDescriptor')


def _revalidate_after_signing():
    ed_val = SamlEdValidator(getPolicyDict_from_json())
    self.ed_val.validate_entitydescriptor(ed_str_new=self.ed_signed, sigval=True)
    if self.ed_val.authz_ok:
        self.status = STATUS_REQUEST_QUEUE
    else:
        self.status = STATUS_REJECTED
