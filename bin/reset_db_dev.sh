#!/usr/bin/env bash

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
APPHOME=$(dirname $scriptsdir)
source $scriptsdir/setenv.sh
export DJANGO_SETTINGS_MODULE=pvzdweb.settings_dev
export PGHOST=devl11

ssh devl11 /home/r2h2/devl/docker/c-pvzdweb-pg-dev/reset_pg_data.sh
sleep 5 # && $APPHOME/pvzdweb/wait_pg_become_ready.sh
rm -f $APPHOME/pvzdweb/database_is_initialized || true

rc=0
$APPHOME/bin/load_testdata.sh || rc=$?
if ((rc>0)); then
    echo "load_testdata failed with code=${rc}"
    exit $rc
fi
