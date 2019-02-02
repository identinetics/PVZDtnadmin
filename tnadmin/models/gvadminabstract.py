from django.db import models

#  Attributdefinitionen laut LDAP-gvat_2-5-1


class GvAdminAbstract(models.Model):
    ''' Basisklasse mit administrativen Attributen '''
    STATUS_ACTIVE = 'active'
    STATUS_CHOICES = ((STATUS_ACTIVE, STATUS_ACTIVE), ('inactive', 'inactive'))
    gvStatus = models.CharField(
        verbose_name='Status',
        default=STATUS_ACTIVE, null=True,
        choices=STATUS_CHOICES,
        db_column='gvstatus',
        max_length=8)
    gvSource = models.CharField(
        verbose_name='Änderung am/durch',
        default='', null=True, blank=True,
        db_column='gvsource',
        max_length=100)
    gvScope = models.CharField(
        default='gv.at', null=True,
        db_column='gvscope',
        max_length=32)

    class Meta:
        abstract = True

    def defined_attr(self) -> list:
        # list replicated attributes _except_ ldap_dn
        return [
            'gvScope',
            'gvSource',
            'gvStatus',
        ]
