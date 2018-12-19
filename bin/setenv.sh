#!/bin/bash -e
# set run time environment with default values for RHEL/Centos7 and macOS

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
export APP_HOME=$(dirname $scriptsdir)

if [[ "$(uname)" == "Linux" ]] && [[ -f /etc/redhat-release ]]; then
    [[ "$JAVA_HOME" ]] || export JAVA_HOME=/etc/alternatives/java_sdk_1.8.0
elif [[ "$(uname)" == "Darwin" ]]; then  # MacOS (Development)
    [[ "$JAVA_HOME" ]] || export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0/Contents/Home
    # Java 9 not yet supported (class loader problem?)
    export DYLD_LIBRARY_PATH=$JAVA_HOME/jre/lib/server
elif [[ ! "$JAVA_HOME" ]]; then
    echo "Critical error: JAVA_HOME not set"
    exit 1
fi

export PYTHONPATH=$PYTHONPATH:$APP_HOME:$APP_HOME/PVZDlib:.
export CLASSPATH="\
$APP_HOME/PVZDlib/MOA-SPSS/moa-sig-lib-latest.jar:\
$APP_HOME/PVZDlib/MOA-SPSS/lib/*:\
$APP_HOME/PVZDlib/unittests/junit-4.11.jar:\
$APP_HOME/PVZDlib/PVZDjava/*"
