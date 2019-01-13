#!/bin/bash -e

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APPHOME=$(dirname $scriptsdir)

python $APPHOME/pep/pep.py