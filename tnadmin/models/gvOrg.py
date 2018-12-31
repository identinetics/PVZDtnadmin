from django.db import models
from tnadmin.models import *

#  Attributdefinitionen laut LDAP-gvat_2-5-1


class GvOrgAbstract(GvAdminAbstract):
    '''
    Gemeinsame Basisklasse für gvOrgUnit und gvOrganization
    Wird benötigt, weil gvOrganization nicht das Feld 'ou' erbt (weil es mandatory wäre).
    '''
    class Meta:
        abstract = True

    gvOuId = models.CharField(
        unique=True,
        verbose_name='gvOuId',
        help_text='Syntax: gvOuId::= Landeskennung ":" ID; ID::= "VKZ:" VKZ | Org-Id  (z.B. AT:VKZ:GGA1234, AT:L9:9876)',
        max_length=32)
    gvOuVKZ = models.CharField(
        unique=True,
        verbose_name='Verwaltungskennz (gvOuVKZ)',
        help_text='Organisationskennzeichen (OKZ) gemäß der Spezifikation [VKZ]. Das Organisationskennzeichen ist für die Verwendung auf Ausdrucken, als Suchbegriff bzw. zur Anzeige vorgesehen. Das OKZ enthält Semantik und ist nur für österreichische Organisationen definiert. Für Referenzen in elektronischen Datenbeständen soll dieses Kennzeichen NICHT verwendet werden, sondern ausschließlich die gvOuId. Das VKZ kann aufgrund von Namensänderungen angepasst werden müssen. (z.B. BMEIA statt BMAA für das Außenministerium)  (z.B. GGA-12345)',
        max_length=32)
    gvOuIdParent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Übergeordnete OE; (gvOuIdParent)',
        null=True, blank=True,
        help_text='gvOuId der übergeordneten OEs (kein dn!)')
    gvOuCn = models.CharField(
        verbose_name='Gesamtbezeichnung (gvOuCn)',
        max_length=1024,
        help_text='Gesamtbezeichnung der Organisationseinheit für die Anschrift ohne Adressteil. (Bundesministerium für Inneres Sektion IV / Abt.ITMS / Ref.NIK)', )
    cn = models.CharField(
        verbose_name='Bezeichnung (cn)',
        help_text='Bezeichnung der Organisationseinheit (ausgeschrieben). (Abt. ITMS/Ref. NIK -  Referat nationale und internationale Koordination)',
        max_length=120)
    mail = models.CharField(
        null=True, blank=True,
        help_text='RFC 822 [RFC882] E-Mail-Adresse  (helpdesk@xyz.gv.at)',
        max_length=256)
    location = models.CharField(
        verbose_name='Ort (l)',
        null=True, blank=True,
        db_column='l',
        help_text='Ort',
        max_length=64)
    description = models.TextField(
        null=True, blank=True,
        help_text='Beschreibung',
        max_length=1024)
    gvNotValidBefore = models.CharField(
        verbose_name='gültig ab',
        null=True, blank=True,
        help_text='JJJJ-MM-TT',
        max_length=10)
    gvNotValidAfter = models.CharField(
        verbose_name='gültig bis',
        null=True, blank=True,
        help_text='Format JJJJ-MM-TT',
        max_length=10)
    c = models.CharField(max_length=250,default='AT')
    co = models.CharField(max_length=250, default='')
    facsimileTelephoneNumber = models.CharField(max_length=250, default='')
    l = models.CharField(db_column='location', max_length=250, default='')
    ou = models.CharField(max_length=250, default='')
    postalAddress = models.CharField(max_length=250, default='')
    postalCode = models.CharField(max_length=250, default='')
    postOfficeBox = models.CharField(max_length=250, default='')
    street = models.CharField(max_length=250, default='')
    telephoneNumber = models.CharField(max_length=250, default='')
    gvImageRef = models.CharField(max_length=250, default='')
    gvLegalSuccessor = models.CharField(max_length=250, default='')
    gvOtherID = models.CharField(max_length=250, default='')
    gvOuId = models.CharField(max_length=250, default='')
    gvOuIdParent = models.CharField(max_length=250, default='')
    gvPhysicalAddress = models.CharField(max_length=250, default='')
    gvSortkey = models.CharField(max_length=250, default='')
    gvWebAddress = models.CharField(max_length=250, default='')

    def save(self, *args, **kwargs):
        self.gvOuId = self.gvOuId.upper()
        self.gvOuVKZ = self.gvOuVKZ.upper()
        super(GvOrgAbstract, self).save(*args, **kwargs)

    # attributes defined in LDAP-gvat_2-5-1_20171222.pdf
    @staticmethod
    def defined_attr() -> list:
        combined_list = GvAdminAbstract().defined_attr()    # cannot super() in static method
        combined_list += [
            'cn',
            'co',
            'description',
            'facsimileTelephoneNumber',
            'gvImageRef',
            'gvLegalSuccessor',
            'gvNotValidAfter',
            'gvNotValidBefore',
            'gvOtherID',
            'gvOuCn',
            'gvOuId',
            'gvOuId',
            'gvOuIdParent',
            'gvOuIdParent',
            'gvOuVKZ',
            'gvPhysicalAddress',
            'gvScope',
            'gvSortkey',
            'gvSource',
            'gvStatus',
            'gvWebAddress',
            'l',
            'mail',
            'postalAddress',
            'postalCode',
            'postOfficeBox',
            'street',
            'telephoneNumber',
        ]
        return combined_list


class GvOrgUnit(GvOrgAbstract):
    class Meta:
        ordering = ['gvOuVKZ']
        verbose_name = 'Organisationseinheit'
        verbose_name_plural = 'Organisationseinheiten'

    # LDAP meta-data
    #base_dn = "dc=at"
    #object_classes = ['gvOrgUnit']

    actions = None

    ou = models.CharField(
        unique=True,
        verbose_name='Kurzbezeichnung (ou)',
        db_column='ou',
        help_text='Kurzbezeichnung der Organisationseinheit (z.B. IV/2b)',
        max_length=64)

    @staticmethod
    def defined_attr() -> list:
        combined_list = GvOrgAbstract().defined_attr()   # cannot super() in static method
        combined_list += ['ou',]
        return combined_list


class GvOrganisation(GvOrgAbstract):
    class Meta:
        ordering = ['o']
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisationen'

    o = models.CharField(
        unique=False,
        verbose_name='Kurzbezeichnung (o)',
        help_text='Kurzbezeichnung der Organisation (z.B. BMI)',
        max_length=64)

    @staticmethod
    def defined_attr() -> list:
        combined_list = GvOrgAbstract().defined_attr()   # cannot super() in static method
        combined_list += ['o',]
        return combined_list