#!/bin/bash -e

# delay until postgres is ready, up to PGSTARTUP_RETRIES seconds
[[ "$PGSTARTUP_RETRIES" ]] || PGSTARTUP_RETRIES=30

scriptsdir=$(cd $(dirname $BASH_SOURCE[0]) && pwd)
python $scriptsdir/set_dotpgpass.py
echo "Waiting for postgres server to start, waiting up to $((PGSTARTUP_RETRIES))s"
until psql -h postgres -U postgres -c 'select 1' -w pvzddb > /dev/null 2>&1 || (( PGSTARTUP_RETRIES == 0 )); do
    PGSTARTUP_RETRIES=$((PGSTARTUP_RETRIES-=1))
    printf '.'
    sleep 1
done
psql -h postgres -U postgres -c 'select 1' -w pvzddb > /dev/null 2>&1 && \
   echo "database available"