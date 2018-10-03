from django.db import models



class MDstatement(models.Model):
    '''
    Metadata Statement (Meldung von neuen/zu aktualisierenden Metadaten)
    '''

    class Meta:
        ordering = ['entityID']
        verbose_name = 'Metadata Statement'

    entityID = models.CharField(unique=True, max_length=128)
    STATUS_UPLOADED = 'uploaded'
    STATUS_REQUEST_QUEUE = 'request_queue'
    STATUS_REJECTED = 'rejected'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = ((STATUS_UPLOADED, STATUS_UPLOADED),
                      (STATUS_REQUEST_QUEUE, STATUS_REQUEST_QUEUE),
                      (STATUS_REJECTED, STATUS_REJECTED),
                      (STATUS_PUBLISHED, STATUS_PUBLISHED),
                       )
    Status = models.CharField(
        verbose_name='Status',
        default=STATUS_UPLOADED, null=True,
        choices=STATUS_CHOICES,
        max_length=14)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField(auto_now=True)
