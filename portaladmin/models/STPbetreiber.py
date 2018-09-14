from django.db import models



class STPbetreiber:
    '''
    Stammportalbetreiber als Teilmenge von gvOrg., Wird nicht in LDAP, sondern im Policy-Journal gespeichert
    '''

    class Meta:
        ordering = ['gvOuID']
        verbose_name = 'STPbetreiber'

    gvOuID = models.CharField(
        unique=True,
        verbose_name='gvOuId',
        max_length=32)
    cn = models.CharField(
        verbose_name='Bezeichnung (cn)',
        db_column='cn',
        help_text='Bezeichnung der Organisationseinheit (ausgeschrieben). (Abt. ITMS/Ref. NIK -  Referat nationale und internationale Koordination)',
        max_length=64)

    def save(self, *args, **kwargs):
        self.gvOuID = self.gvOuID.upper()

