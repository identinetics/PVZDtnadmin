''' Create Postgres ~/.pgpass file from django settings if it does not exist '''

from pathlib import Path

import django
from django.conf import settings


def main():
    django.setup()
    default_db = create_pgpass_entry(settings.DATABASES['default'])
    admin_db = create_pgpass_entry(settings.DATABASES['admin_db'])
    write_pgpass([default_db, admin_db])


def create_pgpass_entry(pgdb: str) -> str:
    assert pgdb['ENGINE'] == 'django.db.backends.postgresql'
    format_data = {
        'hostname':  pgdb['HOST'],
        'port': pgdb['PORT'],
        'database': pgdb['NAME'],
        'username': pgdb['USER'],
        'password': pgdb['PASSWORD'],
    }
    return '{hostname}:{port}:{database}:{username}:{password}'.format(**format_data)


def write_pgpass(entries: list) -> None:
    pgpass = Path.home() / '.pgpass'
    if not pgpass.exists():
        with pgpass.open('w') as fd:
            fd.write('\n'.join(entries))
        pgpass.chmod(0o600)


main()
