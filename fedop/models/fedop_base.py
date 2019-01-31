import django.utils.timezone
from django.db import models

class FedopBaseAbstract(models.Model):
    marked4delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum')
    #created_at = models.DateTimeField(verbose_name='Eingangsdatum', default=django.utils.timezone.now())
    #updated_at = models.DateTimeField(verbose_name='Änderungsdatum', default=django.utils.timezone.now())
    added_to_journal = models.BooleanField(default=False)
    deleted_from_journal = models.BooleanField(default=False)

    class Meta:
        abstract = True

