from django.db import models
from PVZDpy.xy509cert import XY509cert


class Issuer(models.Model):
    cacert = models.CharField(
        unique=True,
        verbose_name='CA Certificate',
        help_text='Issuer Certificate (TLS CA)',
        max_length=10000)
    PVPROLE_CHOICES = (('STP', 'STP'),
                       ('AWP', 'AWP'),
                      )
    pvprole = models.CharField(
        verbose_name='Status',
        default='STP', null=True,
        choices=PVPROLE_CHOICES,
        max_length=3)
    subject_cn = models.CharField(
        help_text='Issuer X.509 SubjectCN (TLS CA)',
        max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Eingangsdatum',) #default=django.utils.timezone.now())
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        xy509cert = XY509cert(self.cacert)
        self.subject_cn = xy509cert.getSubjectCN

# Test
class IssuerSTPManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(pvprole='STP')


class IssuerSTP(Issuer):
    objects = IssuerSTPManager()
    class Meta:
        proxy = True
