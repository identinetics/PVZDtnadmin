#!/bin/bash -e
scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APPHOME=$(dirname $scriptsdir)

$scriptsdir/init_database.sh

rc_sum=0

exec_loader() {
    local cmd=$1
    local rc=0
    $cmd || rc=$?
    if ((rc>0)); then
        echo "$cmd failed with code=${rc}"
        rc_sum=$((rc_sum+rc))
    fi
    printf "\n\n\n"
}

if [[ $DJANGO_SETTINGS_MODULE == 'pvzdweb.settings' ]]; then
    export DJANGO_SETTINGS_MODULE='pvzdweb.settings_allapps'
else
    :   # dev environment has already all apps registered
fi

echo 'tnadmin test data: loading gvOrganisation'
exec_loader "python $APPHOME/tnadmin/sync_gvOrg_from_ldapgvat.py --select-all"

echo 'tnadmin test data: loading gvFederationOrg'
exec_loader "python $APPHOME/tnadmin/initial_load_fedorg.py"

echo 'fedop test data: loading various entities'
exec_loader "python $APPHOME/fedop/tests/load_db_with_testdata.py"

echo 'portaladmin test data: MD Statements'
exec_loader "python $APPHOME/portaladmin/tests/load_db_with_testdata.py"

exit $rc_sum