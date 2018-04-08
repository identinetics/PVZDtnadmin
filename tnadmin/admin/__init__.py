from tnadmin.admin.gvFederation import *
from tnadmin.admin.gvFederationOrg import *
from tnadmin.admin.gvOrg import *
from tnadmin.admin.gvUserPortal import *
from django.contrib import auth

admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)