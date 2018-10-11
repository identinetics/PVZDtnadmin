from datetime import timedelta

from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction
from django.conf import settings

from .models import CheckOut, MDstatement
from .signals import *


@receiver(md_statement_edit_starts)
def create_remove_md_statement_checkout(sender, **kwargs):
    md_statement = kwargs.get('md_statement', None)
    user = kwargs.get('current_user', None)

    if not (md_statement or user):
        return

    # logic of check out creation

    delta_min = getattr(settings, 'PORTALADMIN_CHECKOUT_MINUTES', 15)
    datetime_ago = timezone.now() - timedelta(minutes=delta_min)

    # try to get CheckOut for current user

    if md_statement.checkout_status:
        if md_statement.checkout_status.checkout_by == user:
            # reset check out time
            md_statement.checkout_status.created_at = timezone.now()
            md_statement.checkout_status.save()
        else:
            # remove all checkout another user check out and create new if < datetime_15_min_ago
            if md_statement.checkout_status.created_at < datetime_ago:
                with transaction.atomic():
                    md_statement.checkout_status.delete()
                    check_out = CheckOut.objects.create(checkout_by=user)
                    md_statement.checkout_status = check_out
                    md_statement.save(update_fields=['checkout_status'])

    else:  # if not locked
        with transaction.atomic():
            check_out = CheckOut.objects.create(checkout_by=user)
            md_statement.checkout_status = check_out
            md_statement.save(update_fields=['checkout_status'])





