#!/bin/bash -e
scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APPHOME=$(dirname $scriptsdir)

if [[ ! -e "$APPHOME/database/database_initialized" ]]; then
    echo 'database schema has not been created yet'
    $scriptsdir/init_database.sh
    touch $APPHOME/database/database_initialized
else
    echo 'database already initialized'
fi

# load testdata
python $APPHOME/tnadmin/sync_gvOrg_from_ldapgvat.py
python $APPHOME/tnadmin/initial_load_fedorg.py
python $APPHOME/fedop/tests/load_db_with_testdata.py
python $APPHOME/portaladmin/tests/load_db_with_testdata.py
