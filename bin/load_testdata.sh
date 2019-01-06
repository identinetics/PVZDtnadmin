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

echo 'loading gvOrganisation'
python $APPHOME/tnadmin/sync_gvOrg_from_ldapgvat.py
printf "\n\n\n"
echo 'loading gvFederationOrg'
python $APPHOME/tnadmin/initial_load_fedorg.py
printf "\n\n\n"
echo 'loading fedop test data'
python $APPHOME/fedop/tests/load_db_with_testdata.py
printf "\n\n\n"
echo 'loading test federation entities'
python $APPHOME/portaladmin/tests/load_db_with_testdata.py
