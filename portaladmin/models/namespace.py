from django.db import models
from portaladmin.models import Portalbetreiber


class Namespace:
    fqdn = models.CharField(
        unique=True,
        verbose_name='Namespace',
        help_text='fully qualified domain name or domain with * for any hostname, such as "*.sso.xyz.org"',
        max_length=128)
    gvOuIdParent = models.ForeignKey(
        Portalbetreiber,
        on_delete=models.PROTECT,
        help_text='OrgID des Portalbetreibers')

    def save(self, *args, **kwargs):
        self.fqdn = self.fqdn.lower()


