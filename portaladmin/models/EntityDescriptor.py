from django.db import models
import json
import tempfile

from .constants import *
from PVZDpy.samled_validator import SamlEdValidator
from django.conf import settings
from ..policydict import getPolicyDict_from_json


class EntityDescriptor(models.Model):
    class Meta:
        abstract = True
        ordering = ['updated_at']
        verbose_name = 'Metadaten Statement'

    def __init__(self, *args, **kw):
        super(MDstatementAbstract, self).__init__(*args, **kw)
        self._ed_uploaded_old = self.ed_uploaded
        self._ed_signed_old = self.ed_signed

    pub_status = models.CharField(
        verbose_name='Status',
        default=PUB_STATUS_PUBLISHED, null=True,
        choices=PUB_STATUS_CHOICES,
        max_length=14)
    ed_published = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor',
        help_text='SAML EntityDescriptor (geprüft, nicht signiert)',
        max_length=100000)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum', )

    def get_entityID(self):
        self.validate()
        eid = self.ed_val.entityID
        if eid:
            return eid
        else:
            return '?'
    get_entityID.short_description = 'entityID'

    @property
    def updated(self):
        return self.updated_at.strftime("%Y%m%d %H:%M")

    def get_signer_subject(self):
        self.validate()
        return getattr(self.ed_val, 'signer_cert_cn', False)
    get_signer_subject.short_description = 'Signiert von'


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
