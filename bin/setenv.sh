#!/bin/bash -e
# set run time environment with default values for RHEL/Centos7 and macOS

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
export APPHOME=$(dirname $scriptsdir)

if [[ "$(uname)" == "Linux" ]] && [[ -f /etc/redhat-release ]]; then
    [[ "$JAVA_HOME" ]] || export JAVA_HOME=/etc/alternatives/java_sdk_1.8.0
elif [[ "$(uname)" == "Darwin" ]]; then  # MacOS (Development)
    [[ "$JAVA_HOME" ]] || export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)
    # Java 9 not yet supported (class loader problem?)
    #export DYLD_LIBRARY_PATH=$JAVA_HOME/jre/lib/server
    #export DYLD_LIBRARY_PATH=$JAVA_HOME/lib/server
elif [[ ! "$JAVA_HOME" ]]; then
    echo "Critical error: JAVA_HOME not set"
    exit 1
fi

export PYTHONPATH=$PYTHONPATH:$APPHOME:$APPHOME/PVZDlib:.
export CLASSPATH="\
$APPHOME/PVZDlib/MOA-SPSS/moa-sig-lib-latest.jar:\
$APPHOME/PVZDlib/MOA-SPSS/lib/*:\
$APPHOME/PVZDlib/unittests/junit-4.11.jar:\
$APPHOME/PVZDlib/PVZDjava/*"
