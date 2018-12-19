''' Create Postgres ~/.pgpass file from django settings '''

import os
from pathlib import Path
import sys
import django
if __name__ == '__main__':
    django_proj_home = Path(sys.argv[0]).parent.parent.resolve()
    sys.path.append(django_proj_home)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pvzdweb.settings")
    django.setup()
else:
    assert False

from django.conf import settings

pgdb = settings.DATABASES['default']

assert pgdb['ENGINE'] == 'django.db.backends.postgresql'

format_data = {
    'hostname':  pgdb['HOST'],
    'port': pgdb['PORT'],
    'database': pgdb['NAME'],
    'username': pgdb['USER'],
    'password': pgdb['PASSWORD'],
}
dotpgpass_template = '{hostname}:{port}:{database}:{username}:{password}'.format(**format_data)

pgpass = Path.home() / '.pgpass'
if not pgpass.exists():
    with pgpass.open('w') as fd:
        fd.write(dotpgpass_template)
    pgpass.chmod(0o600)
