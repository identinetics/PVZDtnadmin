import django
django.setup()
from tnadmin.models.gvorg import *

qs = GvOrganisation.objects.all()
for o in qs:
    if o.gvouvkz not in ('L9', 'XFN-160573m', 'BKA', 'BMI', 'BMJ', 'XFN-318886a'):
        try:
            o.delete()
        except Exception:
            pass