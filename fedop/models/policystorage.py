from django.db import models


class PolicyStorage(models.Model):
    ''' singleton '''
    policy_journal_xml = models.BinaryField(
        verbose_name='Policy Journal signed',
        help_text='Policy Journal signed with an enveloping XML signature',
        )
    policy_journal_json = models.TextField(
        verbose_name='Policy Journal unsigned (JSON)',
        help_text='Policy Journal (non authoritative)',
        default='',
        )
    policy_dict_json = models.TextField(
        verbose_name='Policy Journal unsigned (JSON)',
        )
    policy_dict_html = models.TextField(
        verbose_name='Policy Journal HTML',
        help_text='Policy Journal unsigned (HTML)',
        )
    shibacl = models.BinaryField(
        verbose_name='ShibSP ACL',
        )
    trustedcerts_report = models.TextField(
        verbose_name='Trusted certs',
        help_text=' list (fedop + portaladmin, non-authoritative)',
        )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum', )

    class Meta:
        verbose_name = 'Policy Storage'
        verbose_name_plural = 'Policy Storage'

    def save(self, *args, **kwargs):
        self.id=1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

