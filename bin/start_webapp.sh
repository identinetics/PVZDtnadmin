#!/usr/bin/env bash

SCRIPTDIR=$(cd $(dirname $BASH_SOURCE[0]) && pwd)
PROJ_HOME=$(cd $(dirname $SCRIPTDIR) && pwd)
export PYTHONPATH=$PROJ_HOME:$PROJ_HOME/PVZDlib

# As a rule-of-thumb set the --workers according to the following formula: 2 * CPUs + 1
gunicorn pvzdweb.wsgi:application \
    --workers=3 \
    --access-logfile - \
    --bind 0.0.0.0:8080
