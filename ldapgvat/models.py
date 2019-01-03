from django.contrib.postgres.fields import ArrayField
import ldapdb.models
from ldapdb.models.fields import CharField, ImageField, IntegerField, ListField


class OrganizationalUnit(ldapdb.models.Model):
    class Meta:
        abstract = True
    # base_dn and primary_key not defined

    object_classes = ['OrganizationalUnit']
    c = CharField(db_column='c', max_length=40)
    cn = CharField(db_column='cn', max_length=250)
    co = CharField(db_column='co', max_length=250)
    description = CharField(db_column='description', max_length=65000)
    facsimileTelephoneNumber = CharField(db_column='facsimileTelephoneNumber', max_length=250)
    l = CharField(db_column='location', max_length=250)
    mail = CharField(db_column='mail', max_length=250)
    ou = CharField(db_column='ou', max_length=250)
    postalAddress = CharField(db_column='postalAddress', max_length=2000)
    postalCode = CharField(db_column='postalCode', max_length=20)
    postOfficeBox = CharField(db_column='postOfficeBox', max_length=10)
    street = CharField(db_column='street', max_length=250)
    telephoneNumber = CharField(db_column='telephoneNumber', max_length=250)

    def __str__(self):
        return self.cn

    def __repl__(self):
        return self.dn


class gvOrgUnit(OrganizationalUnit):
    base_dn = "dc=at"
    object_classes = ['gvOrgUnit']
    # RDN == Primary Key

    gvImageRef = CharField(db_column='gvImageRef', max_length=250)
    gvLegalSuccessor = CharField(db_column='gvLegalSuccessor', max_length=250)
    gvNotValidAfter = CharField(db_column='gvNotValidAfter', max_length=12)
    gvNotValidBefore = CharField(db_column='gvNotValidBefore', max_length=12)
    gvOtherID = CharField(db_column='gvOtherID', max_length=250)
    gvOuCn = CharField(db_column='gvOuCn', max_length=250)
    gvOuId = CharField(db_column='gvOuId', max_length=250, primary_key=True)  # this maps to the LDAP RDN
    gvOuIdParent = CharField(db_column='gvOuIdParent', max_length=250)
    gvOuVKZ = CharField(db_column='gvOuVKZ', max_length=250)
    gvPhysicalAddress = CharField(db_column='gvPhysicalAddress', max_length=250)
    gvSortkey = CharField(db_column='gvSortkey', max_length=25)
    gvWebAddress = CharField(db_column='gvWebAddress', max_length=250)

    gvScope = CharField(db_column='gvScope', max_length=250)
    gvSource = CharField(db_column='gvSource', max_length=250)
    gvStatus = CharField(db_column='gvStatus', max_length=250)


class GvOrganisation(gvOrgUnit):
    o  = CharField(db_column='o', max_length=250)


class GvUserPortal(ldapdb.models.Model):
    base_dn = "dc=at"
    object_classes = ['gvUserPortal']
    # RDN == Primary Key: cn is list field _only_ using a single value by convention

    cn = CharField(db_column='cn', max_length=250, primary_key=True)
    description = CharField(db_column='description', max_length=1024)
    gvAdminContactMail = ArrayField(CharField(db_column='gvadmincontactmail ', max_length=256),)
    gvAdminContactName = ArrayField(CharField(db_column='gvadmincontactname', max_length=256),)
    gvAdminContactTel = ArrayField(CharField(db_column='gvadmincontacttel', max_length=32),)
    gvDefaultParticipant = CharField(db_column='gvdefaultparticipant', max_length=32)
    gvMaxSecClass = IntegerField(db_column='gvmaxsecclass')
    gvParticipants = ArrayField(CharField(db_column='gvparticipants', max_length=32), size=5000)
    gvPortalHotlineMail = ArrayField(CharField(db_column='gvportalhotlinemail', max_length=250),)
    gvSupportedPvpProfile = ArrayField(CharField(db_column='gvsupportedpvpprofile', max_length=1024),)

    gvScope = CharField(db_column='gvScope', max_length=250)
    gvSource = CharField(db_column='gvSource', max_length=250)
    gvStatus = CharField(db_column='gvStatus', max_length=250)

    def __str__(self):
        return self.cn

    def __repl__(self):
        return self.dn
