import os
os.environ.setdefault('DJANGO_SECRET_KEY', '234089723450987')
import django
django.setup()
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
u = User.objects.get(username='rhoerbe')
u.firstname='t'
u.last_name='est'
u.save()
g = Group.objects.all()
print(str(g))
u.groups.set(g)
u.save()