from django.db import models
from PVZDpy.xy509cert import XY509cert


class Revocation(models.Model):
    cert = models.CharField(
        unique=True,
        verbose_name='Zertifikat',
        help_text='X.509 cert PEM ohne Whitespace; Dieses Zertifikat darf nicht mehr in einem EntityDescriptor verwendet werden',
        max_length=10000)
    subject_cn = models.CharField(
        help_text='X.509 SubjectCN (TLS CA)',
        default='',
        max_length=256)
    issuer_cn = models.CharField(
        help_text='X.509 IssuerCN (TLS CA)',
        default='',
        max_length=256)
    not_after = models.CharField(
        help_text='X.509 not valid after',
        default='',
        max_length=30)
    pubkey = models.CharField(
        help_text='X.509 Public Key (PEM)',
        default='',
        max_length=1000)


    def save(self, *args, **kwargs):
        self.issuer_cn = XY509cert(self.cert).getIssuer_str()
        self.not_after = XY509cert(self.cert).notAfter_str()
        self.pubkey = XY509cert(self.cert).get_pubkey()
        self.subject_cn = XY509cert(self.cert).getSubject_str()
        super().save(*args, **kwargs)