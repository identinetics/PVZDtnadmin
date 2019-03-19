# created manually
import logging
import os
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tnadmin', '0001_initial'),
    ]

    operations = []
    if 'SQLLITE' in os.environ.keys():
        logging.info('Skipping postgres-specific schema modification ')
    else:
        operations = [
            migrations.RunSQL(
                "ALTER TABLE tnadmin_gvorganisation ADD CONSTRAINT gvOuVKZ_maxlen_32 CHECK (length(gvOuVKZ) <= 32);"
            ),
            migrations.RunSQL(
                "ALTER TABLE tnadmin_gvorganisation ADD CONSTRAINT l_maxlen_64 CHECK (length(l) <= 64);"
            ),
            migrations.RunSQL(
                "ALTER TABLE tnadmin_gvorganisation ADD CONSTRAINT o_maxlen_64 CHECK (length(o) <= 64);"
            ),
        ]
