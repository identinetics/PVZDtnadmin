from django.db import models
from tnadmin.models.gvAdminAbstract import *
from tnadmin.models.gvOrg import GvOrganisation

#  Attributdefinitionen laut LDAP-gvat_2-5-1


class GvFederation(GvAdminAbstract):
    '''
    Gemeinsame Basisklasse für gvOu und gvOrganization
    Wird benötigt, weil gvOrganization nicht das Feld 'ou' erbt (weil es mandatory wäre).
    '''
    class Meta:
        verbose_name = 'Federation'
        verbose_name_plural = 'Federations'

    gvFederationName = models.CharField(
        unique=True,
        verbose_name='Federation Name',
        help_text='Eindeutige Bezeichnung einer Federation im E-Mail-Adressen Format nach RFC 822 '
                  'beziehungsweise als DNS Name. Das Zeichen SLASH darf nicht verwendet werden. '
                  'Für den Portalverbund der österreichischen Behörden gem. Portalverbundvereinbarung'
                  'ist als gvFederationName der Wert portalverbund.gv.at festgelegt.'
                  'Organisationsinterne Federations SOLLEN mit "internal@" + Domain-Name der '
                  'Organisation. (z.B. intern@lfrz.at) bezeichnet werden.',
        max_length=64)
    gvMetaDataURL = models.URLField(
        unique=True,
        verbose_name='Metadata URL',
        help_text='Bezugspunkt für Metadaten dieser Federation (URL für signiertes SAML Metadata Aggregat)',
        max_length=200)
    gvDefaultFederation = models.BooleanField(
        default=False,
        verbose_name='default',
        help_text='Setzt die Federation beim Erstellen einer Federation Organisation')
    gvOuId = models.ForeignKey(
        GvOrganisation,
        related_name='Depositar',
        on_delete=models.CASCADE,
        verbose_name='gvOuId',
        null=True, blank=True,
        help_text='gvOuId des Depositars/Federation Operators')

    def __str__(self):
        return self.gvFederationName
