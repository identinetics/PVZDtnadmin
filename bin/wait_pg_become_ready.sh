#!/bin/bash -e
#PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'

# delay until postgres is ready, up to PGSTARTUP_RETRIES seconds
[[ "$PGSTARTUP_RETRIES" ]] || PGSTARTUP_RETRIES=10
[[ "$PGHOST" ]] || PGHOST='PGHOST_not_set'

for i in $(seq 1 5); do
    getent hosts $PGHOST >/dev/null || rc=$?
    if ((rc>0)); then
        printf '-'
        sleep 1
    fi
done

if ((rc>0)); then
    getent hosts $PGHOST || rc=$?
    printf "\nPostgres host ${PGHOST} not available gentent=${rc}\n"
    exit 1
fi

scriptsdir=$(cd $(dirname $BASH_SOURCE[0]) && pwd)
python $scriptsdir/set_dotpgpass.py
echo "Waiting for postgres server to start, waiting up to $((PGSTARTUP_RETRIES))s"
until psql -h $PGHOST -U postgres -c 'select 1' -w pvzddb > /dev/null 2>&1 || (( PGSTARTUP_RETRIES == 0 )); do
    PGSTARTUP_RETRIES=$((PGSTARTUP_RETRIES-=1))
    printf '.'
    sleep 1
done
psql -h $PGHOST -U postgres -c 'select 1' -w pvzddb > /dev/null 2>&1 || rc=$?
if ((rc==0)); then
   echo "database available"
else
   echo "database not available on $PGHOST"
   exit 1
fi
