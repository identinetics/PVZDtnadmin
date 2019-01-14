from django.db import models
from PVZDpy.xy509cert import XY509cert
from tnadmin.models import GvUserPortalOperator


class Userprivilege(models.Model):
    class Meta:
        ordering = ['subject_cn']
        unique_together = ['cert', 'gvouid_parent']
        verbose_name = 'Portaladmin (Userprivilege)'
        verbose_name_plural = 'Portaladmins (Userprivilege)'

    cert = models.TextField(
        verbose_name='Portaladminsitrator-Zertifikat',
        help_text='X.509 cert PEM ohne Whitespace',
        max_length=20000)
    gvouid_parent = models.ForeignKey(
        GvUserPortalOperator,
        db_column='gvouid_parent',
        on_delete=models.PROTECT,
        help_text='OrgID des Portalbetreibers')
    subject_cn = models.CharField(
        verbose_name='Name (cn)',
        null=True, blank=True,
        help_text='Vor- und Familienname des Zertifikatsinhabers',
        max_length=254)
    org_cn = models.CharField(
        verbose_name='Name (cn)',
        null=True, blank=True,
        help_text='Berechtigt für Org',
        max_length=254)
    not_after = models.CharField(
        help_text='X.509 not valid after',
        default='',
        max_length=30)

    #@property
    #def cert_teaser(self):
    #    return self.cert[6:56]

    def save(self, *args, **kwargs):
        self.not_after = XY509cert(self.cert).notAfter_str()
        self.org_cn = self.gvouid_parent.gvouid.cn
        self.subject_cn = XY509cert(self.cert).getSubjectCN()
        super().save(*args, **kwargs)

