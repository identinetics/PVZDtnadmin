#!/usr/bin/env bash

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
PROJ_HOME=$(dirname $scriptsdir)

rm -f $PROJ_HOME/database/db.sqlite3

# Create super-user
[[ $DEFAULT_USER ]] || DEFAULT_USER="admin"
[[ $DEFAULT_EMAIL ]] || DEFAULT_EMAIL="admin@local"
[[ $DEFAULT_PASS ]] || DEFAULT_PASS="adminadmin"
$PROJ_HOME/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DEFAULT_USER', '$DEFAULT_EMAIL', '$DEFAULT_PASS')" | $PROJ_HOME/manage.py shell


# load testdata
cd $PROJ_HOME
python fedop/tests/load_db_with_testdata.py