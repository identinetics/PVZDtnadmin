#!/bin/bash -e
scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APP_HOME=$(dirname $scriptsdir)

if [[ ! -e "$APP_HOME/database/database_initialized" ]]; then
    echo 'database schema has not been created yet'
    $scriptsdir/init_database.sh
    touch $APP_HOME/database/database_initialized
else
    echo 'database already initialized'
fi

# load testdata
cd $APP_HOME
python ./tnadmin/tests/sync_gvOrg_from_ldapgvat.py
python ./tnadmin/tests/initial_load_fedorg.py
python ./fedop/tests/load_db_with_testdata.py
python ./portaladmin/tests/load_db_with_testdata.py
cd -