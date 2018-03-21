from django.db import models
from django.core.validators import MaxValueValidator
from tnadmin.models.gvAdminAbstract import GvAdminAbstract
from tnadmin.models.gvFederation import GvFederation
from tnadmin.models.gvOrg import GvOrganisation

#  Attributdefinitionen laut LDAP-gvat_2-5-1


class GvUserPortal(GvAdminAbstract):
    class Meta:
        verbose_name = 'Stammportal'
        verbose_name_plural = 'Stammportale'

    cn = models.CharField(
        unique=True,
        verbose_name='Bezeichnung',
        help_text='Eindeutige Bezeichnung des Stammportals im Email-Format (pvpportal@noel.gv.at)',
        max_length=64)
    gvOuIdOwner = models.ForeignKey(
        GvOrganisation,
        related_name='Portalbetreiber',
        on_delete=models.CASCADE,
        verbose_name='Portalbetreiber',
        null=True, blank=True,
        help_text='gvOuId des Stammportalbetreibers (Organisation des Portalverantwortlichen')
    gvOuIdParticipant = models.ForeignKey(
        GvOrganisation,
        related_name='Participant',
        on_delete=models.CASCADE,
        verbose_name='Participant',
        null=True, blank=True,
        help_text='Liste der zugriffsberechtigten Stelle (gvOrganisation), die das Stammportal '
                  'benutzen, als gvOuId')
    gvMaxSecClass = models.PositiveIntegerField(
        validators=[MaxValueValidator(3)],
        verbose_name='Max Sicherheitsklasse',
        help_text='Maximale gvSecClass, die Benutzer eines Portal erreichen können (z.B. 0). '
                  'Anwendungsfälle sind vor allem Test- und Entwicklungsportale. ')
    description = models.TextField(
        null=True, blank=True,
        help_text='Beschreibung',
        max_length=1024)
    gvFederationNames = models.ManyToManyField(
        GvFederation,
        through='GvUserPortalFederationInfo')
    gvSamlIdpEntityId = models.URLField(
        null=True, blank=True,
        verbose_name='EntityID',
        help_text='Eindeutiger Identifier des Stammportal in einer SAML Federation (URI)',
        max_length=80)

    def __str__(self):
        return self.cn


class GvUserPortalFederationInfo(GvAdminAbstract):
    class Meta:
        verbose_name = 'Stammportal-Federation'
        verbose_name_plural = 'Stammportal-Federations'

    class Meta:
        auto_created = True
    gvFederationName = models.ForeignKey(
        GvFederation,
        on_delete=models.CASCADE,
        verbose_name='Federation',
        null=True, blank=True,
        help_text='Federation, in die das Stammportal eingebunden ist')
    gvUserPortal = models.ForeignKey(
        GvUserPortal,
        on_delete=models.CASCADE,
        verbose_name='Federation',
        null=True, blank=True,
        help_text='Federation, in die das Stammportal eingebunden ist')
