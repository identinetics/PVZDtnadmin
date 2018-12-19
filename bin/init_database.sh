#!/bin/bash -e

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APP_HOME=$(dirname $scriptsdir)

rm -f $APP_HOME/database/db.sqlite3

# Create super-user
[[ $DEFAULT_USER ]] || DEFAULT_USER="admin"
[[ $DEFAULT_EMAIL ]] || DEFAULT_EMAIL="admin@local"
[[ $DEFAULT_PASS ]] || DEFAULT_PASS="adminadmin"
$APP_HOME/manage.py migrate && echo "Initial database migration complete"
echo "from django.contrib.auth.models import User; "\
     "User.objects.create_superuser('$DEFAULT_USER', "\
     "'$DEFAULT_EMAIL', '$DEFAULT_PASS')" |\
     $APP_HOME/manage.py shell && echo 'DB superuser created'

touch $APP_HOME/database/database_initialized