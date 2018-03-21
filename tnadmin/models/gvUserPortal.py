from django.db import models
from django.core.validators import MaxValueValidator
from tnadmin.models.gvAdminAbstract import gvAdminAbstract
from tnadmin.models.gvOrg import gvOrganisation

#  Attributdefinitionen laut LDAP-gvat_2-5-1


class gvUserPortal(gvAdminAbstract):
    class Meta:
        verbose_name = 'Stammportal'
        verbose_name_plural = 'Stammportale'

    cn = models.CharField(
        unique=True,
        verbose_name='Bezeichnung',
        help_text='Eindeutige Bezeichnung des Stammportals im Email-Format (pvpportal@noel.gv.at)',
        max_length=64)
    gvOuIdOwner = models.ForeignKey(
        gvOrganisation,
        on_delete=models.CASCADE,
        verbose_name='Portalbetreiber',
        null=True, blank=True,
        help_text='gvOuId des Stammportalbetreibers (Organisation des Portalverantwortlichen')
    gvMaxSecClass = models.PositiveIntegerField(
        validators=[MaxValueValidator(3)],
        verbose_name='Max Sicherheitsklasse',
        help_text='Maximale gvSecClass, die Benutzer eines Portal erreichen können (z.B. 0). '
                  'Anwendungsfälle sind vor Allem Test- und Entwicklungsportale. ')
    description = models.TextField(
        null=True, blank=True,
        help_text='Beschreibung',
        max_length=1024)

    def __str__(self):
        return self.cn
