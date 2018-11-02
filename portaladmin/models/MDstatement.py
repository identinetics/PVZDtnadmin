from django.db import models
import json
import tempfile

from PVZDpy.aodsfilehandler import AODSFileHandler
from PVZDpy.invocation.aodsfhinvocation import aodsfhInvocation
from PVZDpy.aodslisthandler import AodsListHandler
from PVZDpy.invocation.aodslhinvocation import aodslhInvocation
from PVZDpy.samled_pvp import SAMLEntityDescriptorPVP
from PVZDpy.userexceptions import *
from django.conf import settings



def getPolicyDict_from_journal() -> dict:

    aods_filename = settings.PVZD_SETTINGS['policyjournal']
    trustedcerts_filename = settings.PVZD_SETTINGS['trustedcerts']
    aodsfh_invocation = aodsfhInvocation(aods_filename, trustedcerts_filename)
    aodsFileHandler = AODSFileHandler(aodsfh_invocation)
    aodsfh_invocation = aodslhInvocation(
        inputfilename=aods_filename,
        trustedcerts=trustedcerts_filename)
    aodsListHandler = AodsListHandler(aodsFileHandler, aodsfh_invocation)
    return aodsListHandler.aods_read()


class CheckOut(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    checkout_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class MDstatementAbstract(models.Model):
    @staticmethod
    def getPolicyDict_from_json() -> dict:
        with open(settings.PVZD_SETTINGS['policydir']) as fd:
            return json.load(fd)

    STATUS_CREATED = 'created'
    STATUS_UPLOADED = 'uploaded'
    STATUS_REQUEST_QUEUE = 'request_queue'
    STATUS_REJECTED = 'rejected'
    STATUS_ACCEPTED = 'accepted'
    STATUS_CHOICES = ((STATUS_CREATED, 'erstellt'),
                      (STATUS_UPLOADED, 'hochgeladen'),
                      (STATUS_REQUEST_QUEUE, 'signiert und eingebracht'),
                      (STATUS_REJECTED, 'fehlerhaft'),
                      (STATUS_ACCEPTED, 'akzeptiert'),
                      )
    status = models.CharField(
        verbose_name='Status',
        default=STATUS_UPLOADED, null=True,
        choices=STATUS_CHOICES,
        max_length=14)
    ed_uploaded = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor uploaded',
        help_text='SAML EntityDescriptor (uploaded, signiert)',
        max_length=100000)
    ed_signed = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor signiert',
        help_text='SAML EntityDescriptor (signiert)',
        max_length=100000)
    delete = models.BooleanField(
        default=False,
        help_text='EntitiyDescriptor vom Metadaten Aggregat löschen',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def entityID(self):
        if self.ed_uploaded:
            if not getattr(self, 'policydir', False):
                self.policydir = self.getPolicyDict_from_json()
            fd = tempfile.NamedTemporaryFile(mode='w', prefix='pvzd_', suffix='.xml')
            fd.write(self.ed_uploaded)
            fd.flush()
            try:
                entityID = SAMLEntityDescriptorPVP(fd.name, self.policydir).get_entityID()
            except(Exception) as e:
                entityID = e.__class__.__name__ + ': ' + str(e)
            fd.close()
        else:
            entityID = ''
        return entityID

    def __str__(self):
        return str(self.entityID)

    class Meta:
        abstract = True
        ordering = ['updated_at']
        verbose_name = 'Metadaten Statement'


class MDstatement(MDstatementAbstract):

    checkout_status = models.ForeignKey(CheckOut, blank=True,
                                        related_name="md_statements",
                                        null=True, on_delete=models.SET_NULL)
    # TODO create signal to save history

# class MDstatement(models.Model):
#     """
#     Metadata Statement (Meldung von neuen/zu aktualisierenden Metadaten)
#     """
#
#     class Meta:
#         abstract = True
#         ordering = ['entityID', 'updated_at']
#
#     entityID = models.CharField(unique=True, max_length=128)
#     STATUS_UPLOADED = 'uploaded'
#     STATUS_REQUEST_QUEUE = 'request_queue'
#     STATUS_REJECTED = 'rejected'
#     STATUS_PUBLISHED = 'published'
#     STATUS_DELETED = 'deleted'
#     STATUS_CHOICES = ((STATUS_UPLOADED, 'hochgeladen'),
#                       (STATUS_REQUEST_QUEUE, 'signiert und eingebracht'),
#                       (STATUS_REJECTED, 'fehlerhaft'),
#                       (STATUS_PUBLISHED, 'veröffentlicht'),
#                       (STATUS_DELETED, 'gelöscht'),
#                       )
#     Status = models.CharField(
#         verbose_name='Status',
#         default=STATUS_UPLOADED, null=True,
#         choices=STATUS_CHOICES,
#         max_length=14)
#     Validation_message = models.CharField(blank=True, null=True, max_length=1000)
#     ed_uploaded = models.TextField(
#         blank=True, null=True,
#         verbose_name='EntityDescriptor uploaded',
#         help_text='SAML EntityDescriptor (uploaded, signiert)',
#         max_length=100000)
#     ed_signed = models.TextField(
#         blank=True, null=True,
#         verbose_name='EntityDescriptor signiert',
#         help_text='SAML EntityDescriptor (signiert)',
#         max_length=100000)
#     delete = models.BooleanField(
#         default=False,
#         help_text='EntitiyDescriptor vom Metadaten Aggregat löschen',
#     )
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
#     updated_at = models.DateTimeField(auto_now=True)
#
#     checkout_status = models.ForeignKey(CheckOut, blank=True,
#                                         related_name="md_statements",
#                                         null=True, on_delete=models.SET_NULL)
#
#     def __str__(self):
#         return str(self.entityID)
