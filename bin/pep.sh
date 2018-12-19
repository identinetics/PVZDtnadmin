#!/bin/bash -e

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APP_HOME=$(dirname $scriptsdir)

python $APP_HOME/pep/pep.py