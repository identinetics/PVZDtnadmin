from django.db import models

class Issuer(models.Model):
    cacert = models.CharField(
        unique=True,
        verbose_name='Namespace',
        help_text='fully qualified domain name',
        max_length=128)
    pvprole = models.CharField(
        verbose_name='Name (cn)',
        help_text='Vor- und Familienname des Zertifikatsinhabers',
        max_length=64)
    subjectCN = models.CharField(
        max_length=128)


