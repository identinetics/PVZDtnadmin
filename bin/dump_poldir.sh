#!/bin/bash

# dump policy directory to git, for review and use by frontend authorization

SCRIPTDIR=$(dirname $BASH_SOURCE[0])
source $SCRIPTDIR/setEnv.sh
source $SCRIPTDIR/setConfig.sh

echo "$PVZDPOLMAN_VERSION (dump_poldir.sh)"

args=$@
mkdir -p $POLMAN_REPODIR/unsigned/history
$py3 $PROJ_HOME/src/PMP.py read \
    --journal $POLMAN_REPODIR/unsigned/history/policyjournal.json \
    --poldirhtml $POLMAN_REPODIR/unsigned/policydir.html \
    --poldirjson $POLMAN_REPODIR/unsigned/policydir.json \
    --shibacl $POLMAN_REPODIR/unsigned/shibacl.json