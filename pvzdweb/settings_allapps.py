from pvzdweb.settings import *

INSTALLED_APPS=sorted(list(set(INSTALLED_APPS + ['fedop', 'ldapgvat', 'portaladmin', 'tnadmin'])))
