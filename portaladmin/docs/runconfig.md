= Run Configuration

The run configuration needs to be provided from outside, such as a docker container or IDE.
For Linux the script bin/setenv.sh provides an automated detection.

== PYTHON

The python virtual env needs to have python3>=3.4 with the packages from requirements.txt installed.  

The PYTHONPATH needs the project root and library root set, i.e.
$PROJ_HOME:$PROJHOME/PVZDlib/PVZDpy

The testrunner (pytest) also requires the respective test/ folder, 
e.g. by setting the PYTHONPATH to the current directory and starting test scripts from there. 

== DJANGO

The production site requires the env variable SECRET_KEY to be set to a random value during initial configuration, e.g.:
openssl rand -base64 30

== JAVA

The Portaladmin app that uses library functions that do Signature and XML-validation with Java classes. 
The environment must provide CLASSPATH and JAVA_HOME, and for MacOS DYLD_LIBRARY_PATH, too.
PYJNIUS_ACTIVATE has to be set (without value) as well.

== Example for MacOS development environment

export CLASSPATH=/Users/admin/devl/python/identinetics/PVZDweb/PVZDlib/MOA-SPSS/moa-sig-lib-latest.jar:/Users/admin/devl/python/identinetics/PVZDweb/PVZDlib/MOA-SPSS/lib/*:/Users/admin/devl/python/identinetics/PVZDweb/PVZDlib/unittests/junit-4.11.jar:/Users/admin/devl/python/identinetics/PVZDweb/PVZDlib/PVZDjava/*
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0/Contents/Home
export DYLD_LIBRARY_PATH=/Library/Java/JavaVirtualMachines/jdk1.8.0/Contents/Home/jre/lib/server
export PYJNIUS_ACTIVATE=

export PYTHONPATH=/Users/admin/devl/python/identinetics/PVZDweb:/Users/admin/devl/python/identinetics/PVZDweb/portaladmin:/Users/admin/devl/python/identinetics/PVZDweb/PVZDlib

Further examples can be found in bin/