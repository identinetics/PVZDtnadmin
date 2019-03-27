#!/bin/bash -e

# The python virtual env needs to be set

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
APPHOME=$(dirname $scriptsdir)

source $scriptsdir/setenv.sh


# test PVZDlib/PVZDpy
cd $APPHOME/PVZDlib/PVZDpy/tests

pytest -m "not requires_signature" -v --cov=PVZDpy --ignore=test_cresignedxml.py .


# Need to run portaladmin/tests/test_mdstatement_api.py separately because of yet undiscovered side-effect
cd $APPHOME

pytest -m "not requires_signature" -m "not show_testenv" \
    -v --ignore=PVZDlib --ignore=portaladmin/tests/test_mdstatement_api.py \
    --cov=cli --cov=fedop  --cov=portaladmin  --cov=tnadmin

pytest -v -m "not show_testenv" --tb=short portaladmin/tests/test_mdstatement_api.py


