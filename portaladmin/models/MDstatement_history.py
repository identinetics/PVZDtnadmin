from django.db import models
from django.conf import settings


class MDstatementHistory(models.Model):
    """
    Metadata Statement History (loaded from git)

    """

    class Meta:
        ordering = ['entityID', 'updated_at']
        verbose_name = 'Metadaten Statement History'

    entityID = models.ForeignKey(="MDstatements", on_delete=models.CASCADE)
    Status = models.CharField(
        verbose_name='Status',
        choices=STATUS_CHOICES,
        max_length=14)
    Validation_message = models.CharField(blank=True, null=True, max_length=1000)
    ed_uploaded = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor uploaded',
        max_length=100000)
    ed_signed = models.TextField(
        blank=True, null=True,
        verbose_name='EntityDescriptor signiert',
        max_length=100000)
    created_at = models.DateTimeField(verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField()

    def __str__(self):
        return str(self.entityID)
