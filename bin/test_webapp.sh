#!/bin/bash -e

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
source $scriptsdir/setenv.sh
APP_HOME=$(dirname $scriptsdir)


# FYI: curl -s = Don't show download progress, -o /dev/null = don't display the body,
# -w "%{http_code}" = Write http response code to stdout after exit

