#!/bin/bash

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
PROJ_HOME=$(dirname $scriptsdir)

python $PROJ_HOME/pep/pep.py