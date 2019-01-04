from django.db import models
from tnadmin.models.gvAdminAbstract import *
from tnadmin.models.gvorg import GvOrganisation

#  Attributdefinitionen laut LDAP-gvat_2-5-1


class GvFederation(GvAdminAbstract):
    ''' singleton '''
    class Meta:
        verbose_name = 'Federation'
        verbose_name_plural = 'Federation'

    gvfederationname = models.CharField(
        unique=True,
        verbose_name='Federation Name',
        help_text='Eindeutige Bezeichnung der Federation im E-Mail-Adressen Format nach RFC 822 '
                  'beziehungsweise als DNS Name. Das Zeichen SLASH darf nicht verwendet werden. '
                  'Für den Portalverbund der österreichischen Behörden gem. Portalverbundvereinbarung'
                  'ist als gvfederationname der Wert portalverbund.gv.at festgelegt.'
                  'Organisationsinterne Federations SOLLEN mit "internal@" + Namespace-Name der '
                  'Organisation. (z.B. intern@lfrz.at) bezeichnet werden.',
        max_length=64)
    gvmetadataurl = models.URLField(
        unique=True,
        verbose_name='Metadata URL',
        help_text='Bezugspunkt für Metadaten dieser Federation (URL für signiertes SAML Metadata Aggregat)',
        max_length=200)

    def __str__(self):
        return self.gvfederationname
