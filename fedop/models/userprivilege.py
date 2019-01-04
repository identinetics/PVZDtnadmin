from django.db import models
from tnadmin.models import GvUserPortalOperator


class Userprivilege(models.Model):
    class Meta:
        ordering = ['cn']

    cert = models.TextField(
        unique=True,
        verbose_name='Portaladminsitrator-Zertifikat',
        help_text='X.509 cert PEM ohen Whitespace',
        max_length=20000)
    gvOuIdParent = models.ForeignKey(
        GvUserPortalOperator,
        db_column='gvouid_parent',
        on_delete=models.PROTECT,
        help_text='OrgID des Portalbetreibers')
    cn = models.CharField(
        verbose_name='Name (cn)',
        null=True, blank=True,
        help_text='Vor- und Familienname des Zertifikatsinhabers',
        max_length=64)

    @property
    def org_cn(self):
        return self.gvOuIdParent.cn

    @property
    def cert_teaser(self):
        return self.cert[:60]

