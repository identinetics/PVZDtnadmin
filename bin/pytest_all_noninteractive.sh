#!/bin/bash -e

# The python virtual env needs to be set

scriptsdir=$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)
[[ "$APPHOME" ]] || APPHOME=$(dirname $scriptsdir)

source $scriptsdir/setenv.sh


# test PVZDlib/PVZDpy
cd $APPHOME/PVZDlib/PVZDpy/tests

pytest -m "not requires_signature" -v --cov=PVZDpy --ignore=test_cresignedxml.py .


# Need to run portaladmin/tests/test_mdstatement_api.py separately because of yet undiscovered side-effect
cd $APPHOME

# pytest with collection and coverage was working with commit 27bcab01a, but had problems with test_mdstatement_model.
# refactoring broke it. quickt fix to split pytest invocations
#pytest -m "not requires_signature" -m "not show_testenv" \
#    -v --ignore=PVZDlib --ignore=portaladmin/tests/test_mdstatement_api.py \
#    --cov=cli --cov=fedop  --cov=portaladmin  --cov=tnadmin

#pytest -v -m "not show_testenv" --tb=short portaladmin/tests/test_mdstatement_api.py

exec_pytest() {
    pytest -v -m "not show_testenv" -m "not requires_webapp" --tb=short --ignore PVZDlib $1
}


exec_pytest ./fedop/tests/test_aodsfilehandler.py
exec_pytest ./fedop/tests/test_fedop_models.py
exec_pytest ./fedop/tests/test_poljournal_updater.py
exec_pytest ./fedop/tests/test_pvzdlib_config.py
exec_pytest ./ldapgvat/tests/test_ldapgvat_models.py
exec_pytest ./portaladmin/tests/test_mdstatement_model.py
exec_pytest ./portaladmin/tests/test_sign_sigproxy.py
exec_pytest ./tnadmin/tests/test_tnadmin_models.py
