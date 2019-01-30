#!/bin/bash

SCRIPTDIR=$(dirname $BASH_SOURCE[0])
source $SCRIPTDIR/setEnv.sh
source $SCRIPTDIR/setConfig.sh

echo "$PVZDPOLMAN_VERSION (PMP)"

args=$@
$py3 $PROJ_HOME/src/PMP.py ${args:='--help'}
