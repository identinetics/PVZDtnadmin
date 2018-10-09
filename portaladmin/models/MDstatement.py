from django.db import models

from django.conf import settings


class CheckOut(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    checkout_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class MDstatement(models.Model):
    """
    Metadata Statement (Meldung von neuen/zu aktualisierenden Metadaten)
    """

    class Meta:
        ordering = ['entityID']
        verbose_name = 'Metadaten Statement'

    entityID = models.CharField(unique=True, max_length=128)
    STATUS_UPLOADED = 'uploaded'
    STATUS_INVALID = 'invalid'
    STATUS_REQUEST_QUEUE = 'request_queue'
    STATUS_REJECTED = 'rejected'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = ((STATUS_UPLOADED, 'hochgeladen'),
                      (STATUS_INVALID, 'Validierungsfehler'),
                      (STATUS_REQUEST_QUEUE, 'signiert und eingebracht'),
                      (STATUS_REJECTED, 'fehlerhaft'),
                      (STATUS_PUBLISHED, 'veröffentlicht'),
                      )
    Status = models.CharField(
        verbose_name='Status',
        default=STATUS_UPLOADED, null=True,
        choices=STATUS_CHOICES,
        max_length=14)
    Validation_message = models.CharField(max_length=1000)
    ed_uploaded = models.TextField(
        verbose_name='EntityDescriptor uploaded',
        help_text='SAML EntityDescriptor (uploaded, signiert)',
        max_length=100000)
    ed_signed = models.TextField(
        verbose_name='EntityDescriptor signiert',
        help_text='SAML EntityDescriptor (signiert)',
        max_length=100000)
    delete = models.BooleanField(
        default=False,
        help_text='EntitiyDescriptor vom Metadaten Aggregat löschen',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField(auto_now=True)

    checkout_status = models.ForeignKey(CheckOut, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.entityID)
