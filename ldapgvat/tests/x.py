import django
import os
import sys
if __name__ == '__main__':
    django_proj_path = os.path.dirname(os.path.dirname(os.getcwd()))
    sys.path.append(django_proj_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
    django.setup()
else:
    assert False
from ldapgvat.models import *

o = gvOrganisation.objects.get(dn='gvOuId=AT:TEST:1,dc=gv,dc=at')
#o = gvOrganisation.objects.get(gvOuId='AT:TEST:1')
assert o.gvStatus == 'active'


