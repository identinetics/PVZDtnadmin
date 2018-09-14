from django.db import models



class MDstatement:
    '''
    Metadata Statement (Meldung von neuen/zu aktualisierenden Metadaten)
    '''

    class Meta:
        ordering = ['entityID']
        verbose_name = 'Metadata Statement'

    entityID = models.CharField(unique=True, max_length=128)
    STATUS_ACTIVE = 'active'
    STATUS_CHOICES = ((STATUS_UPLOADED,
                       GIT_REQUESTQUEUE,
                       GIT_REJECTED,
                       GIT_PUBLISHED,
                       ), (
                       'uploaded',
                       'request_queue',
                       'rejected',
                       'published',
                      ))
    Status = models.CharField(
        verbose_name='Status',
        default=STATUS_UPLOADED, null=True,
        choices=STATUS_CHOICES,
        max_length=14)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum', )
    updated_at = models.DateTimeField(auto_now=True)
