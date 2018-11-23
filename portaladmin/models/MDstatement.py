from django.db import models
import json
import tempfile

from .constants import *
from PVZDpy.samled_validator import SamlEdValidator
from django.conf import settings


class CheckOut(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    checkout_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class MDstatementAbstract(models.Model):
    class Meta:
        abstract = True
        ordering = ['updated_at']
        verbose_name = 'Metadaten Statement'

    def __init__(self, *args, **kw):
        super(MDstatementAbstract, self).__init__(*args, **kw)
        self._ed_uploaded_old = self.ed_uploaded
        self._ed_signed_old = self.ed_signed

    status = models.CharField(
        verbose_name='Workflow Status',
        default=STATUS_CREATED, null=True,
        choices=STATUS_CHOICES,
        max_length=14)
    ed_file_upload = models.FileField(
        upload_to='upload/', default='', null=True, blank=True,
        verbose_name='EntityDescriptor hochladen',)
    ed_uploaded = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor hochgeladen',
        help_text='SAML EntityDescriptor (geladen, nicht signiert)',
        max_length=100000)
    ed_uploaded_filename = models.CharField(
        verbose_name='Upload Filename',
        default=None, null=True,
        max_length=100)
    ed_signed = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor signiert',
        help_text='SAML EntityDescriptor (signiert)',
        max_length=100000)
    admin_note = models.TextField(
        blank=True, null=True,
        verbose_name='Admin Notiz',
        max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum', )

    def is_delete(self):
        self.validate()
        return self.ed_val.deletionRequest
    is_delete.short_description = 'delete entity'

    def get_entityID(self):
        self.validate()
        eid = self.ed_val.entityID
        if eid:
            return eid
        else:
            return '?'

    get_entityID.short_description = 'entityID'

    def get_validation_message(self):
        self.validate()
        if getattr(self.ed_val, 'val_mesg_dict', False):
            return json.dumps(self.ed_val.val_mesg_dict, indent=2)
        else:
            return ''
    get_validation_message.short_description = 'validation message'

    def get_validation_message_trunc(self):
        self.validate()
        if getattr(self.ed_val, 'val_mesg_dict', False):
            m = json.dumps(self.ed_val.val_mesg_dict, indent=2)
            m = m[0:47]+'...' if len(m) > 47 else m
            return m
        else:
            return ''
    get_validation_message_trunc.short_description = 'error'

    @property
    def valid(self):
        self.validate()
        if getattr(self.ed_val, 'content_val_ok', False):
            return self.ed_val.content_val_ok
        else:
            return False

    @property
    def updated(self):
        return self.updated_at.strftime("%Y%m%d %H:%M")

    @property
    def authorized(self):
        self.validate()
        if getattr(self.ed_val, 'authz_ok', False):
            return False
        else:
            return self.ed_val.authz_ok

    def get_signer_subject(self):
        self.validate()
        return getattr(self.ed_val, 'signer_cert_cn', False)
    get_signer_subject.short_description = 'Signiert von'


    def get_boilerplate_help(self):
        return "Ein Metadaten Statement wird erstellt und geändert, indem eine Datei mit einem " \
               "SAML Entity Descriptor hochgeladen wird. Für die Signatur ist in der Listansicht " \
               "der Eintrag zu markieren und die Aktion zum signieren auszuführen."
    get_boilerplate_help.short_description = ''


    def __str__(self):
        self.validate()
        if getattr(self.ed_val, 'entityID', False):
            return str(self.ed_val.entityID)
        else:
            return ''

    def validate(self):
        if not getattr(self, 'ed_val', None):
            self.ed_val = SamlEdValidator(self.getPolicyDict_from_json())
        if self.ed_signed:
            self.ed_val.validate_entitydescriptor(ed_str_new=self.ed_signed, sigval=True)
        elif self.ed_uploaded:
            self.ed_val.validate_entitydescriptor(ed_str_new=self.ed_uploaded, sigval=False)
        pass

    @staticmethod
    def getPolicyDict_from_json() -> dict:
        with open(settings.PVZD_SETTINGS['policydir']) as fd:
            return json.load(fd)

    def save(self, *args, **kwargs):
        if self.ed_file_upload and self.ed_file_upload.file:
            self.ed_uploaded = self.ed_file_upload.file.read().decode('utf-8')
            self.ed_signed = None
        if self.ed_uploaded:
            if self.ed_uploaded != self._ed_uploaded_old and \
               self.status in (STATUS_CREATED, STATUS_REJECTED):
                self.status = STATUS_UPLOADED
                self.ed_uploaded_filename = self.ed_file_upload.file.name
                super().save(*args, **kwargs)
        else:
            self.status = STATUS_CREATED
            self.ed_uploaded_filename = self.ed_file_upload.file.name
            super().save(*args, **kwargs)
        pass

class MDstatement(MDstatementAbstract):

    checkout_status = models.ForeignKey(CheckOut, blank=True,
                                        related_name="md_statements",
                                        null=True, on_delete=models.SET_NULL)
