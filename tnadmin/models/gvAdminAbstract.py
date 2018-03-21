from django.db import models

#  Attributdefinitionen laut LDAP-gvat_2-5-1



class gvAdminAbstract(models.Model):
    ''' Basisklasse mit administrativen Attributen '''
    class Meta:
        abstract = True

    STATUS_ACTIVE = 'active'
    STATUS_CHOICES = ((STATUS_ACTIVE, STATUS_ACTIVE), ('inactive', 'inactive'))
    gvStatus = models.CharField(
        verbose_name='Status',
        default=STATUS_ACTIVE, null=True,
        choices=STATUS_CHOICES,
        db_column='gvStatus',
        max_length=8)
    gvSource = models.CharField(
        verbose_name='Änderung am/durch',
        default='', null=True, blank=True,
        db_column='gvSource',
        max_length=10)
    gvScope = models.CharField(
        default='gv.at', null=True,
        db_column='gvScope',
        max_length=32)

