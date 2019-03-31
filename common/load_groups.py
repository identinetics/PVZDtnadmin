import django
django.setup()
from django.contrib.auth.models import Group


for g in ('fedop', 'portaladmin', 'tnadmin'):
    group = Group(name=g)
    try:
        group.save()
    except django.db.utils.IntegrityError:
        pass
