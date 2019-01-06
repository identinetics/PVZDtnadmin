import datetime
from django.db import models
from django.core.validators import MaxValueValidator
from tnadmin.models.constants import *
from tnadmin.models.get_defaults import *
from tnadmin.models.gvadminabstract import GvAdminAbstract
from tnadmin.models.gvfederation import GvFederation
from tnadmin.models.gvorg import GvOrganisation
from tnadmin.models.gvuserportal import *


#  Attributdefinitionen laut LDAP-gvat_2-5-1

class GvFederationOrg(GvAdminAbstract):
    class Meta:
        ordering = ('gvouid',)
        unique_together = (('gvouid', 'gvouid_aufsicht', 'gvouid_dl', 'gvContractStatus'),)
        verbose_name = 'Federation Member'
        verbose_name_plural = 'Federation Members'

    gvouid = models.ForeignKey(
        GvOrganisation,
        related_name='Vertragspartei',
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Vertragspartei (berechtigt)',
        help_text='gvOuId der Vertragspartei in der Rolle Teilnehmer, zugriffsberechtige Stelle oder Dienstleister')
    gvouid_aufsicht = models.ForeignKey(
        GvOrganisation,
        related_name='VertragsparteiPVV',
        on_delete=models.PROTECT,
        null=False, blank=True,
        default=get_default_org(),
        verbose_name='Vertragspartei (Aufsicht)',
        help_text='gvOuId der Vertragspartei in der Rolle "Vertreter des Depositars"')
    gvouid_dl = models.ForeignKey(
        GvOrganisation,
        related_name='Dienstleister',
        on_delete=models.PROTECT,
        null=False, blank=True,
        default=get_default_org(),
        verbose_name='Dienstleister',
        help_text='gvOuId des Dienstleister')
    gvContractStatus = models.CharField(
        verbose_name='Rechtsgrundlage',
        db_column='gvcontractstatus',
        null=False,
        choices=LEGAL_BASIS_CHOICES,
        max_length=30)
    gvDateEffective = models.DateField(
        default=datetime.date.today,
        verbose_name='Gültig Ab',
        db_column = 'gvdateeffective', )
    gvDateTerminated = models.DateField(
        null=True, blank=True,
        verbose_name='Gültig bis',
        db_column='gvdateterminated', )
    gvCaseNumber = models.CharField(
        null=True, blank=True,
        verbose_name='Ablagereferenz',
        db_column='gvcasenumber',
        help_text='Geschäftszahlen/Referenzen für Antrag, Vertrag und Änderungen',
        max_length=500)
    gvCaseOrg = models.ForeignKey(
        GvOrganisation,
        related_name='BearbeiterOrganisation',
        on_delete=models.DO_NOTHING,
        verbose_name='Bearbeitende Organisation (VKZ)',
        db_column='gvcaseorg',
        null=True, blank=True,
        help_text='gvOuId der Organisation die den Antrag bearbeitet (i.A. der Depositar)')
    description = models.TextField(
        null=True, blank=True,
        help_text='Kommentare',
        max_length=10000)

    def __str__(self):
        return f"{self.gvouid.gvouid} {self.gvouid.cn}"

    def __repr__(self):
        return f"id={self.id}; {self.gvouid.gvouid}"


class GvParticipantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gvContractStatus__in=LEGAL_BASIS_PARTICIPANT).order_by('gvouid__gvouid')


class GvParticipant(GvFederationOrg):
    objects = GvParticipantManager()
    class Meta:
        ordering = ('gvouid',)
        proxy = True
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'


class GvUserPortalOperatorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gvContractStatus__in=LEGAL_BASIS_IDP_OP).order_by('gvouid__gvouid')


class GvUserPortalOperator(GvFederationOrg):
    objects = GvUserPortalOperatorManager()
    class Meta:
        proxy = True
        verbose_name = 'STP-Betreiber'
        verbose_name_plural = 'STP-Betreiber'
