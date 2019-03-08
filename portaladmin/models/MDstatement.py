import base64
import hashlib
import json
import tempfile
from typing import Optional
from django.conf import settings
from django.db import models

from portaladmin.constants import STATUS_ACCEPTED, STATUS_CREATED, STATUS_REJECTED, STATUS_CHOICES, STATUS_UPLOADED, \
    STATUSGROUP_BACKEND, STATUSGROUP_FRONTEND, STATUSGROUP_CHOICES
from django.core.exceptions import ValidationError
from PVZDpy.config.pvzdlib_config_abstract import PVZDlibConfigAbstract
from PVZDpy.policydict import PolicyDict
from PVZDpy.samled_validator import SamlEdValidator
from fedop.models.namespace import Namespaceobj


#class CheckOut(models.Model):
#    created_at = models.DateTimeField(auto_now_add=True)
#    checkout_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class MDstatement(models.Model):
    class Meta:
        #abstract = True
        ordering = ['-updated_at']
        verbose_name = 'Metadaten Statement'
        unique_together = (('entityID', 'make_blank_entityid_unique', 'statusgroup'), )

    def __init__(self, *args, **kw):
        super(MDstatement, self).__init__(*args, **kw)
        self._ed_uploaded_old = self.ed_uploaded
        self.policy_dict = PolicyDict()

    admin_note = models.TextField(
        blank=True, null=True,
        verbose_name='Admin Notiz',
        max_length=1000)
    allow_selfsigned = models.BooleanField(
        default=False, null=False,
        verbose_name='Selbst-signiertes Zertifikat OK',
        help_text='Selbst-signiertes oder nicht registriertes Zertifikat erlauben (nicht für PVP-R-Profil)')
    content_valid = models.BooleanField(
        default=False, null=False,
        verbose_name='Content validation', )
    deletionRequest = models.BooleanField(
        default=False, null=True,
        verbose_name='Deletion Request (unpublish Entity)', )
    ed_file_upload = models.FileField(
        upload_to='portaladmin', default='', null=True, blank=True,
        verbose_name='EntityDescriptor hochladen',)
    ed_signed = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor signiert',
        help_text='SAML EntityDescriptor (signiert)',
        max_length=100000)
    ed_uploaded = models.TextField(  # do not write this field directly, always upload into ed_file_upload
        blank=False, null=False, default='',
        verbose_name='EntityDescriptor hochgeladen',
        help_text='SAML EntityDescriptor (geladen, nicht signiert)',
        max_length=100000)
    ed_uploaded_filename = models.CharField(
        verbose_name='Upload Filename',
        default=None, null=True,
        max_length=257)
    entityID = models.CharField(
        blank=True, null=True, default='',
        max_length=301)
    entity_fqdn = models.CharField(
        blank=True, null=True,
        verbose_name='Entity FQDN',
        max_length=300)
    make_blank_entityid_unique = models.CharField(
        verbose_name = 'if the entityID is blank due to a validation error, this hash value '
                       'assures that the unique constraint is not violated',
        blank=True, null=True, default='',
        max_length=16)
    operation = models.CharField(
        blank=True, null=True,
        max_length=7)
    org_cn = models.CharField(
        blank=True, null=True,
        verbose_name='Organization',
        max_length=60)
    org_id = models.CharField(
        blank=True, null=True,
        verbose_name='OrgID',
        max_length=20)
    signer_authorized = models.BooleanField(
        default=False, null=True,
        verbose_name='Signer Authorization', )
    signer_subject = models.CharField(
        blank=True, null=True,
        verbose_name='Signator',
        max_length=80)
    status = models.CharField(
        verbose_name='Workflow Status',
        default=STATUS_CREATED, null=False,
        choices=STATUS_CHOICES,
        max_length=14)
    statusgroup = models.CharField(
        verbose_name='Status Group', null=False,
        default=STATUSGROUP_FRONTEND,
        choices=STATUSGROUP_CHOICES,
        max_length=8)
    validation_message  = models.TextField(
        blank=True, null=True,
        verbose_name='Error Messages',
        max_length=100000)
    namespace = models.CharField(
        blank=True, null=True,
        max_length=30)
#    namespace = models.ForeignKey(  # TODO: clarifiy if foreign key is possible to enforce referential integrity
#        Namespaceobj,
#        blank=True, null=True,
#        on_delete=models.PROTECT,
#        help_text='Namespace')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum', )

    @property
    def updated(self):
        return self.updated_at.strftime("%Y%m%d %H:%M")

    def get_validation_message_trunc(self):
        if self.validation_message:
            m = json.dumps(self.validation_message, indent=2)[1:-1]
            m = m.replace('\\n','').replace('\\"','"').replace('{','').replace('"','')
            m = m[0:47]+'...' if len(m) > 47 else m
            return m
        else:
            return ''
    get_validation_message_trunc.short_description = 'error'


    def get_boilerplate_help(self):
        return "Ein Metadaten Statement wird erstellt und geändert, indem eine Datei mit einem " \
               "SAML Entity Descriptor hochgeladen wird. Mit der Signatur wird das Dokument zur Veröffentlichung eingebracht."
    get_boilerplate_help.short_description = ''


#-------
    def serialize_json(self):
        """ serialize stable values for unit tests """
        dictfilt = lambda d, filter: dict([(k, d[k]) for k in d if k in set(filter)])
        wanted_keys = (
            'admin_note',
            'ed_signed',
            'ed_uploaded',
            'entityID',
            'status',
        )
        self_dict = dictfilt(self.__dict__, wanted_keys)
        return json.dumps(self_dict, sort_keys=True, indent=2)

    def __str__(self):
        s = (self.entityID or self._get_make_blank_entityid_unique() or '')
        return s

    def __repr__(self):
        r = f"{self.entityID} {self.statusgroup} {self._get_make_blank_entityid_unique()}"
        return r

    def validate(self):
        if not getattr(self, 'ed_val', None):
            self.ed_val = SamlEdValidator(self.policy_dict)
        if self.ed_signed:
            self.ed_val.validate_entitydescriptor(
                ed_str_new=self.ed_signed, portaladmin_sigval=True, keydesc_certval=(not self.allow_selfsigned))
        elif self.ed_uploaded:
            self.ed_val.validate_entitydescriptor(
                ed_str_new=self.ed_uploaded, portaladmin_sigval=False, keydesc_certval=(not self.allow_selfsigned))

    def clean(self):
        def _fail_if_updating_not_allowed():
            if self.status == STATUS_ACCEPTED:
                raise ValidationError('Cannot change if status = ' + STATUS_ACCEPTED,
                                      code='invalid')

        def _require_upload_for_change():
            if not self.ed_file_upload.name:
                raise ValidationError('Ein neuer EntityDescriptor muss hochgeladen werden')

        _fail_if_updating_not_allowed()
        _require_upload_for_change()

    def save(self, *args, **kwargs):
        def _read_uploaded_file():
            if self.ed_file_upload.name:
                self.ed_uploaded = self.ed_file_upload.file.read().decode('utf-8')
        def _set_status_on_upload():
            if self.ed_uploaded != self._ed_uploaded_old:
                if self.status in (STATUS_CREATED, STATUS_REJECTED):
                    self.status = STATUS_UPLOADED
        def _set_computed_fields():
            self.validate()
            self.content_valid = self._is_content_valid()
            self.deletionRequest = self.ed_val.deletionRequest
            self.ed_uploaded_filename = self.ed_file_upload.file.name if self.ed_file_upload else None
            self.entity_fqdn = self._get_fqdn()
            self.entityID = self._get_entityID()
            self.make_blank_entityid_unique = self._get_make_blank_entityid_unique()
            self.namespace_id = self._get_namespace_id()
            self.operation = self._get_operation()
            self.org_cn = self._get_orgcn()
            self.org_id = self._get_orgid()
            self.signer_authorized = self._is_authorized()
            self.signer_subject = getattr(self.ed_val, 'signer_cert_cn', '')
            self.statusgroup = self._get_statusgroup()
            self.validation_message = self._get_validation_message()
        def _enforce_unique_constraint():
            if self._state.adding:
                qs = MDstatement.objects.filter(
                    entityID=self.entityID,
                    make_blank_entityid_unique=self.make_blank_entityid_unique,
                    statusgroup=self.statusgroup)
                if qs:
                    raise ValidationError(f"Der EntityDescriptor {self.entityID} ist mit dem Status "
                                           "{qs[0].status} ist bereits vorhanden")

        if kwargs.get('operation', '') == 'mds_sign_and_update':
            super().save(*args, {})
        elif kwargs.get('operation', '') == 'PEP':   # see security considerations in docs/
            super().save(*args, {})
        else:
            _read_uploaded_file()
            _set_status_on_upload()
            _set_computed_fields()
            _enforce_unique_constraint()
            super().save(*args, **kwargs)

    def _get_make_blank_entityid_unique(self) -> Optional[str]:
        ''' enable storing broken <EntityDescriptor> documents where an entityID cannot be parsed '''
        if self.entityID:
            return None
        else:
            hashobj = hashlib.md5()
            hashobj.update(self.ed_uploaded.encode('utf-8'))
            hash_str = base64.a85encode(hashobj.digest()).decode('ascii')[0:16]
            return hash_str

    def _get_entityID(self):
        eid = self.ed_val.entityID
        if eid:
            return eid
        #elif self.ed_uploaded:
        #    return '?' # no more than 1 broken upload allowed
        else:
            return ''

    def _get_fqdn(self):
        fqdn = None
        if getattr(self.ed_val, 'ed', False):
            fqdn = (self.ed_val.ed.get_entityid_hostname() or self.ed_val.ed.get_entityid())
        return (fqdn or self._get_make_blank_entityid_unique())

    def _get_namespace_id(self):
        if getattr(self.ed_val, 'ed', False):
            ns = self.ed_val.ed.get_namespace()
            if ns:
                qs = Namespaceobj.objects.filter(fqdn=ns)
                if qs:
                    return qs[0].id
        return None

    def _get_operation(self):
        if not getattr(self.ed_val, 'ed', False):
            return ''
        if not self.ed_val.ed.get_entityid_hostname():
            return ''
        if self.ed_val.deletionRequest:
            return 'delete'
        if self.status == STATUS_ACCEPTED:
            return 'published'
        return 'add/mod'

    def _get_orgid(self):
        if getattr(self.ed_val, 'ed', False):
            fqdn = self.ed_val.ed.get_entityid_hostname()
            return self.ed_val.policydict.get_orgid(fqdn)

    def _get_orgcn(self):
        if getattr(self.ed_val, 'ed', False):
            return self.ed_val.policydict.get_orgcn(self._get_orgid())

    def _get_statusgroup(self):
        if self.status == STATUS_ACCEPTED:
            return STATUSGROUP_BACKEND
        else:
            return STATUSGROUP_FRONTEND

    def _get_validation_message(self):
        if getattr(self.ed_val, 'val_mesg_dict', False):
            return json.dumps(self.ed_val.val_mesg_dict, indent=2)
        else:
            return ''

    def _is_authorized(self):
        self.validate()
        if getattr(self.ed_val, 'authz_ok', False):
            return False
        else:
            return self.ed_val.authz_ok

    def _is_content_valid(self):
        if getattr(self.ed_val, 'content_val_ok', False):
            return self.ed_val.content_val_ok
        else:
            return False


#class MDstatement(MDstatementAbstract):
#    checkout_status = models.ForeignKey(CheckOut, blank=True,
#                                        related_name="md_statements",
#                                        null=True, on_delete=models.SET_NULL)
