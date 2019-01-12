from pvzdweb.settings_dev import *

# remove portaladmin (and thererfore JAVA dependency)

INSTALLED_APPS = [e for e in INSTALLED_APPS if e not in ('portaladmin', )]
