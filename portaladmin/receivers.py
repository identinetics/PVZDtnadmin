from .signals import *

from django.dispatch import receiver


@receiver(md_statement_edit_starts)
def check_md_statement_checkout(sender, **kwargs):
    # TODO work with checkout status
    pass
