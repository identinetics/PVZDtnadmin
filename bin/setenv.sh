#!/bin/bash
# set run time environment

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
export PROJ_HOME=$(dirname $scriptsdir)

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

export PYJNIUS_ACTIVATE=     # remove this line to use javabridge instead of pyjnius

# --- do not change below this line for target system configuration
export PATH=$PATH:$PROJ_HOME/bin
export PYTHONPATH=$PYTHONPATH:$PROJ_HOME:$PROJ_HOME/PVZDlib:.
export CLASSPATH="\
$PROJ_HOME/PVZDlib/MOA-SPSS/moa-sig-lib-latest.jar:\
$PROJ_HOME/PVZDlib/MOA-SPSS/lib/*:\
$PROJ_HOME/PVZDlib/unittests/junit-4.11.jar:\
$PROJ_HOME/PVZDlib/PVZDjava/*"
