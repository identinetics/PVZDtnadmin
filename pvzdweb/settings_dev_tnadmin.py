from pvzdweb.settings_dev import *

# remove portaladmin (and thererfore dependency)

INSTALLED_APPS = [e for e in INSTALLED_APPS if e != 'portaladmin']
