#!/usr/bin/env bash

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
APPHOME=$(dirname $scriptsdir)
source $scriptsdir/setenv.sh
export DJANGO_SETTINGS_MODULE=pvzdweb.settings_dev

# DOC ONLY, yet untested!

echo 'reset DB to remove migration history and app schema'
ssh devl11 /home/r2h2/devl/docker/c-pvzdweb-pg-dev/reset_pg_data.sh
sleep 5 # && $APPHOME/pvzdweb/wait_pg_become_ready.sh

echo 'temporarily removing custom migration code (tnadmin/migrations/*_custom_migr_*)'
mkdir -p $APPHOME/tnadmin/tmp_makemigrations
mv $APPHOME/tnadmin/migrations/*_custom_migr_* $APPHOME/tnadmin/tmp_makemigrations/

echo 'removing previous migrations'
rm -f $APPHOME/fedop/migrations/0*.py
rm -f $APPHOME/portaladmin/migrations/0*.py
rm -f $APPHOME/tnadmin/migrations/0*.py

$APPHOME/manage.py makemigrations

echo 'removing migration code for ldap'
rm -f $APPHOME/ldapgvat/migrations/0001_initial.py

echo 'restoring custom migration code'
mv $APPHOME/tnadmin/tmp_makemigrations/* $APPHOME/tnadmin/migrations/
rmdir $APPHOME/tnadmin/tmp_makemigrations

echo 'add to git'
git add \
  tnadmin/migrations/0*.py \
  fedop/migrations/0001_initial.py \
  portaladmin/migrations/0001_initial.py
