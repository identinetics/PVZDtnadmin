from django.db import models


class PolicyJournal(models.Model):
    ''' singleton '''
    policy_journal = models.BinaryField(
        verbose_name='Policy Journal',
        help_text='Policy Journal signed with an enveloping XML signature',
        )

    class Meta:
        verbose_name = 'Policy Journal'
        verbose_name_plural = 'Policy Journal'

    updated_at = models.DateTimeField(auto_now=True, verbose_name='Änderungsdatum', )

    def save(self, *args, **kwargs):
        self.id=1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

