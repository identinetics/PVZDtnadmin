from django.db import models
from PVZDpy.xy509cert import XY509cert


class Revocation(models.Model):
    cert = models.CharField(
        unique=True,
        verbose_name='Zertifikat',
        help_text='X.509 cert PEM ohne Whitespace; Dieses Zertifikat darf nicht mehr in einem EntityDescriptor verwendet werden',
        max_length=10000)
    subject_cn = models.CharField(
        help_text='Issuer X.509 SubjectCN (TLS CA)',
        default='',
        max_length=128)
    pubkey = models.CharField(
        help_text='Issuer X.509 Public Key',
        default='',
        max_length=1000)

    def save(self, *args, **kwargs):
        self.subject_cn = XY509cert(self.cert).get_pubkey()
        super().save(*args, **kwargs)