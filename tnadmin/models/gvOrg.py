from django.db import models
from tnadmin.models import *

#  Attributdefinitionen laut LDAP-gvat_2-5-1


class GvOrgAbstract(GvAdminAbstract):
    '''
    Gemeinsame Basisklasse für gvOu und gvOrganization
    Wird benötigt, weil gvOrganization nicht das Feld 'ou' erbt (weil es mandatory wäre).
    '''
    class Meta:
        abstract = True

    gvOuID = models.CharField(
        unique=True,
        verbose_name='Verwaltungskennzeichen (AT:VKZ)',
        db_column='gvOuID',
        max_length=32)
    gvOuVKZ = models.CharField(
        unique=True,
        verbose_name='Organisationskennzeichen (OKZ)',
        db_column='gvOuVKZ',
        help_text='Organisationskennzeichen (OKZ) gemäß der Spezifikation [VKZ]. Das Organisationskennzeichen ist für die Verwendung auf Ausdrucken, als Suchbegriff bzw. zur Anzeige vorgesehen. Das OKZ enthält Semantik und ist nur für österreichische Organisationen definiert. Für Referenzen in elektronischen Datenbeständen soll dieses Kennzeichen NICHT verwendet werden, sondern ausschließlich die gvOuId. Das VKZ kann aufgrund von Namensänderungen angepasst werden müssen. (z.B. BMEIA statt BMAA für das Außenministerium)  (z.B. GGA-12345)',
        max_length=32)
    gvOuIdParent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Übergeordnete OE; (gvOuIdParent)',
        null=True, blank=True,
        db_column='gvOuIdParent',
        help_text='gvOuId der übergeordneten OEs (kein dn!)')
    cn = models.CharField(
        verbose_name='Bezeichnung (cn)',
        db_column='cn',
        help_text='Bezeichnung der Organisationseinheit (ausgeschrieben). (Abt. ITMS/Ref. NIK -  Referat nationale und internationale Koordination)',
        max_length=64)
    gvOuCn = models.TextField(
        verbose_name='Gesamtbezeichnung (gvOuCn)',
        db_column='gvOuCn',
        help_text='Gesamtbezeichnung der Organisationseinheit für die Anschrift ohne Adressteil. (Bundesministerium für Inneres Sektion IV / Abt.ITMS / Ref.NIK)', )
    mail = models.CharField(
        null=True, blank=True,
        db_column='mail', help_text='RFC 822 [RFC882] E-Mail-Adresse  (helpdesk@xyz.gv.at)',
        max_length=256)
    location = models.CharField(
        verbose_name='Ort (l)',
        null=True, blank=True,
        db_column='l',
        help_text='Ort',
        max_length=64)
    description = models.TextField(
        null=True, blank=True,
        db_column='description',
        help_text='Beschreibung',
        max_length=1024)
    gvNotValidBefore = models.CharField(
        verbose_name='gültig ab',
        null=True, blank=True,
        db_column='gvNotValidBefore',
        help_text='JJJJ-MM-TT',
        max_length=10)
    gvNotValidAfter = models.CharField(
        verbose_name='gültig bis',
        null=True, blank=True,
        db_column='gvNotValidAfter',
        help_text='Format JJJJ-MM-TT',
        max_length=10)

    def save(self, *args, **kwargs):
        self.gvOuID = self.gvOuID.upper()
        self.gvOuVKZ = self.gvOuVKZ.upper()
        super(gvOrgAbstract, self).save(*args, **kwargs)


class GvOrgUnit(GvOrgAbstract):
    class Meta:
        verbose_name = 'Organisationseinheit'
        verbose_name_plural = 'Organisationseinheiten'

    # LDAP meta-data
    #base_dn = "dc=at"
    #object_classes = ['gvOrgUnit']

    ordering = ['gvOuVKZ']
    actions = None

    ou = models.CharField(
        unique=True,
        verbose_name='Kurzbezeichnung (ou)',
        db_column='ou',
        help_text='Kurzbezeichnung der Organisationseinheit (z.B. IV/2b)',
        max_length=64)


    def __str__(self):
        return self.gvOuID



class GvOrganisation(GvOrgAbstract):
    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisationen'
    # LDAP meta-data
    #base_dn = "dc=at"
    #object_classes = ['gvOrganisation']
    ordering = ['o']
    actions = None

    o = models.CharField(
        unique=True,
        verbose_name='Kurzbezeichnung (o)',
        db_column='ou',
        help_text='Kurzbezeichnung der Organisation (z.B. BMI)',
        max_length=64)

    def __str__(self):
        return self.gvOuID
