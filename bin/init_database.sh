#!/bin/bash -e

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APPHOME=$(dirname $scriptsdir)

#rm -f $APPHOME/database/db.sqlite3 || true

if [[ ! -e "$APPHOME/pvzdweb/database_is_initialized" ]]; then
    echo 'database schema has not been created yet'
    touch $APPHOME/pvzdweb/database_is_initialized
else
    echo 'database already initialized'
    exit 0
fi

if (( $($APPHOME/manage.py migrate) > 0 )); then
    echo "failed to create database schema, migrate returned with ${rc}"
else
    echo 'Initial database migration complete'
fi


# Create super-user
rc=0
[[ $DEFAULT_USER ]] || DEFAULT_USER="admin"
[[ $DEFAULT_EMAIL ]] || DEFAULT_EMAIL="admin@local"
[[ $DEFAULT_PASS ]] || DEFAULT_PASS="adminadmin"
echo "from django.contrib.auth.models import User; "\
     "User.objects.create_superuser('$DEFAULT_USER', "\
     "'$DEFAULT_EMAIL', '$DEFAULT_PASS')" |\
     $APPHOME/manage.py shell || rc=$?
if ((rc>0)); then
    echo "manage.py createsuperuser failed with ${rc}"
else
    echo 'DB superuser created'
fi

