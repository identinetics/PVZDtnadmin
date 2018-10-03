from django.db import models
from fedop.models import STPbetreiber


class Userprivilege(models.Model):
    class Meta:
        ordering = ['cn']

    cert = models.CharField(
        unique=True,
        verbose_name='Portaladminsitrator-Zertifikat',
        help_text='X.509 cert PEM ohen Whitespace',
        max_length=128)
    gvOuIdParent = models.ForeignKey(
        STPbetreiber,
        on_delete=models.PROTECT,
        help_text='OrgID des Portalbetreibers')
    cn = models.CharField(
        verbose_name='Name (cn)',
        null=True, blank=True,
        help_text='Vor- und Familienname des Zertifikatsinhabers',
        max_length=64)


