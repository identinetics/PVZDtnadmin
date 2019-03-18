import re
from django.db import models
from django.core.validators import MaxLengthValidator, RegexValidator
from tnadmin.models import *
from tnadmin.models.gvadminabstract import *

#  Attributdefinitionen laut LDAP-gvat_2-5-1


class GvOrgAbstract(GvAdminAbstract):
    '''
    Gemeinsame Basisklasse für gvOrgUnit und gvOrganization
    Wird benötigt, weil gvOrganization nicht das Feld 'ou' erbt (weil es mandatory wäre).
    (db_column setzt eineige Felder auf Lowercase zur Vereinfachung von Abfragen in Postgresql.)
    '''
    class Meta:
        abstract = True

    gvouid = models.CharField(max_length=32,
        unique=True,
        verbose_name='gvOuId',
        validators=[RegexValidator(regex=r'^[A-Z:]{10,10}.*', message='OuId erlaubt Kleinbuchstaben erst ab Position 11')],
        help_text='Syntax: gvOuId::= Landeskennung ":" ID; ID::= "VKZ:" VKZ | Org-Id  (z.B. AT:VKZ:GGA1234, AT:L9:9876)',)
    gvouvkz = models.CharField(max_length=79,
        unique=True,
        verbose_name='Verwaltungskennz (gvOuVKZ)',
        validators=[RegexValidator(regex=r'^[A-Z:]{2,2}.*', message='VKZ erlaubt Kleinbuchstaben erst ab Position 3'),
                    MaxLengthValidator(32, '"gvOuVKZ " Limit: 32 char')],
        help_text='Organisationskennzeichen (OKZ) gemäß der Spezifikation [VKZ]. Das Organisationskennzeichen ist für '
                  'die Verwendung auf Ausdrucken, als Suchbegriff bzw. zur Anzeige vorgesehen. Das OKZ enthält Semantik'
                  ' und ist nur für österreichische Organisationen definiert. Für Referenzen in elektronischen '
                  'Datenbeständen soll dieses Kennzeichen NICHT verwendet werden, sondern ausschließlich die gvOuId. '
                  'Das VKZ kann aufgrund von Namensänderungen angepasst werden müssen. (z.B. BMEIA statt BMAA für das '
                  'Außenministerium)  (z.B. GGA-12345)')
    gvouidparent = models.CharField(max_length=32,
        default='',
        verbose_name='Übergeordnete OE; (gvOuIdParent)',
        db_column='gvouid_parent',
        null=True, blank=True,
        help_text='gvOuId der übergeordneten OEs (kein dn!)')  # Foreign Key hier nicht implementiert
    gvOuCn = models.CharField(max_length=1024,
        verbose_name='Gesamtbezeichnung (gvOuCn)',
        db_column='gvoucn',
        help_text='Gesamtbezeichnung der Organisationseinheit für die Anschrift ohne Adressteil. (Bundesministerium für Inneres Sektion IV / Abt.ITMS / Ref.NIK)', )
    gvNotValidBefore = models.CharField(max_length=10,
        verbose_name='gültig ab',
        db_column='gvnotvalidbefore',
        null=True, blank=True,
        help_text='JJJJ-MM-TT',)
    gvNotValidAfter = models.CharField(max_length=10,
        verbose_name='gültig bis',
        db_column='gvnotvalidafter',
        null=True, blank=True,
        help_text='Format JJJJ-MM-TT',)
    gvImageRef = models.CharField(max_length=250, default='', null=True, blank=True,)
    gvLegalSuccessor = models.CharField(max_length=250, default='', null=True, blank=True,)
    gvOtherID = models.CharField(max_length=250, default='', null=True, blank=True,)
    gvPhysicalAddress = models.CharField(max_length=250, default='', null=True, blank=True,)
    gvSortkey = models.CharField(max_length=250, default='', null=True, blank=True,)
    gvWebAddress = models.CharField(max_length=250, default='', null=True, blank=True,)
    gvouid_upper = models.CharField(max_length=250, default='', unique=True, null=True, blank=True,)
    gvouvkz_upper = models.CharField(max_length=250, default='', unique=True, null=True, blank=True,)

    c = models.CharField(max_length=250,default='AT', null=True, blank=True,)
    cn = models.CharField(max_length=1024,
        verbose_name='Bezeichnung (cn)',
        help_text='Bezeichnung der Organisationseinheit (ausgeschrieben). (Abt. ITMS/Ref. NIK -  Referat nationale und internationale Koordination)',
    )
    co = models.CharField(max_length=250, default='', null=True, blank=True,)
    description = models.TextField(max_length=1024,
        null=True, blank=True,
        help_text='Beschreibung',)
    facsimileTelephoneNumber = models.CharField(max_length=250, default='', null=True, blank=True,)
    l = models.CharField(max_length=123,
        verbose_name='Ort (l)',
        null=True, blank=True,
        help_text='Ort',
        validators=[MaxLengthValidator(64, '"l" Limit: 64 char')],)
    mail = models.CharField(max_length=256,
        null=True, blank=True,
        help_text='RFC 822 [RFC882] E-Mail-Adresse  (helpdesk@xyz.gv.at)',)
    ou = models.CharField(max_length=250, default='', null=True, blank=True,)
    postalAddress = models.CharField(max_length=250, default='', null=True, blank=True,)
    postalCode = models.CharField(max_length=250, default='', null=True, blank=True,)
    postOfficeBox = models.CharField(max_length=250, default='', null=True, blank=True,)
    street = models.CharField(max_length=250, default='', null=True, blank=True,)
    telephoneNumber = models.CharField(max_length=250, default='', null=True, blank=True,)

    def save(self, *args, **kwargs):
        self.gvouid_upper = self.gvouid.upper()
        self.gvouvkz_upper = self.gvouvkz.upper()
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
            'gvouid',
            'gvouidparent',
            'gvouvkz',
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

    def __str__(self):
        return f"{self.gvouid} {self.cn}"

    def __repr__(self):
        return self.ldap_dn


class GvOrganisation(GvOrgAbstract):
    class Meta:
        ordering = ['o']
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisationen'

    ldap_dn = models.CharField(max_length=250, default='')
    o = models.CharField(
        unique=False,
        verbose_name='Kurzbezeichnung (o)',
        help_text='Kurzbezeichnung der Organisation (z.B. BMI)',
        max_length=121)  # circumvent hard-coded error message of default MaxLengthValidator missing the field name

    @staticmethod
    def defined_attr() -> list:
        combined_list = GvOrgAbstract().defined_attr()   # cannot super() in static method
        combined_list += ['o',]
        return combined_list