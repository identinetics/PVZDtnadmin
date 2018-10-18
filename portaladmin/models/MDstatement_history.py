from django.db import models
from django.conf import settings


class MDstatementHistory(models.Model):
    """
    Metadata Statement History

    """

    class Meta:
        ordering = ['entityID']
        verbose_name = 'Metadaten Statement History'

    entityID = models.CharField(max_length=128)
    Status = models.CharField(
        verbose_name='Status',
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

    def __str__(self):
        return str(self.entityID)
