import datetime
from django.db import models
from django.core.validators import MaxValueValidator
from tnadmin.models.constants import *
from tnadmin.models.gvAdminAbstract import GvAdminAbstract
from tnadmin.models.gvFederation import GvFederation
from tnadmin.models.gvorg import GvOrganisation
from tnadmin.models.gvUserPortal import *

#  Attributdefinitionen laut LDAP-gvat_2-5-1

def get_default_federationname() -> int:
    try:
        defaultFedName = GvFederation.objects.filter(gvDefaultFederation=True)[0].id
    except IndexError:
        defaultFedName = ''
    return defaultFedName

LEGAL_BASIS_CHOICES = (
    (LEGAL_BASIS_PVV, LEGAL_BASIS_PVV),
    (LEGAL_BASIS_ENTITLED_ORG, LEGAL_BASIS_ENTITLED_ORG),
    (LEGAL_BASIS_PROCESSOR_IDP, LEGAL_BASIS_PROCESSOR_IDP),
    (LEGAL_BASIS_ENTITLED_ORG_PROCESSOR, LEGAL_BASIS_ENTITLED_ORG_PROCESSOR),
)
LEGAL_BASIS_PARTICIPANT = (LEGAL_BASIS_PVV,
                           LEGAL_BASIS_ENTITLED_ORG,
                           LEGAL_BASIS_ENTITLED_ORG_PROCESSOR)
LEGAL_BASIS_IDP_OP = (LEGAL_BASIS_PVV,
                      LEGAL_BASIS_PROCESSOR_IDP)

class GvFederationOrg(GvAdminAbstract):
    class Meta:
        ordering = ('gvouid',)
        unique_together = (('gvouid', 'gvouid2', 'gvouid3'),)
        verbose_name = 'Federation Member'
        verbose_name_plural = 'Federation Members'

    gvouid = models.ForeignKey(
        GvOrganisation,
        related_name='Vertragspartei',
        on_delete=models.CASCADE,
        verbose_name='Vertragspartei (berechtigt)',
        help_text='gvOuId der Vertragspartei in der Rolle Teilnehmer, zugriffsberechtige Stelle oder Dienstleister')
    gvouid2 = models.ForeignKey(
        GvOrganisation,
        related_name='VertragsparteiPVV',
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name='Vertragspartei (Aufsicht)',
        help_text='gvOuId der Vertragspartei in der Rolle "Vertreter des Depositars"')
    gvouid3 = models.ForeignKey(
        GvOrganisation,
        related_name='Dienstleister',
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name='Dienstleister',
        help_text='gvOuId des Dienstleister')
    gvContractStatus = models.CharField(
        verbose_name='Rechtsgrundlage',
        null=False,
        choices=LEGAL_BASIS_CHOICES,
        max_length=30)
    gvDateEffective = models.DateField(
        default=datetime.date.today,
        verbose_name='Gültig Ab')
    gvDateTerminated = models.DateField(
        null=True, blank=True,
        verbose_name='Gültig bis')
    gvCaseNumber = models.CharField(
        null=True, blank=True,
        verbose_name='Ablagereferenz',
        help_text='Geschäftszahlen/Referenzen für Antrag, Vertrag und Änderungen',
        max_length=500)
    gvCaseOrg = models.ForeignKey(
        GvOrganisation,
        related_name='BearbeiterOrganisation',
        on_delete=models.DO_NOTHING,
        verbose_name='Bearbeitende Organisation (VKZ)',
        null=True, blank=True,
        help_text='gvOuId der Organisation die den Antrag bearbeitet (i.A. der Depositar)')
    description = models.TextField(
        null=True, blank=True,
        help_text='Kommentare',
        max_length=10000)


    #def __str__(self):
    #    return self.gvouid + '/' + self.gvContractStatus + ' (' + self.gvUserPortalName + ')'


class GvParticipantManager(models.Manager):
    def get_queryset(self):
        return super(GvParticipantManager, self).get_queryset().filter(gvContractStatus__in=LEGAL_BASIS_PARTICIPANT)


class GvParticipant(GvFederationOrg):
    objects = GvParticipantManager()
    class Meta:
        proxy = True
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'


class GvUserPortalOperatorManager(models.Manager):
    def get_queryset(self):
        return super(GvUserPortalOperatorManager, self).get_queryset().filter(gvContractStatus__in=LEGAL_BASIS_IDP_OP)


class GvUserPortalOperator(GvFederationOrg):
    objects = GvUserPortalOperatorManager()
    class Meta:
        proxy = True
        verbose_name = 'STP-Betreiber'
        verbose_name_plural = 'STP-Betreiber'
