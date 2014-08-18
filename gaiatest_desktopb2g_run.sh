#!/bin/bash

GAIA_BRANCH=${GAIA_BRANCH:-"master"}
DESKTOPB2G_DIR=${DESKTOPB2G_DIR:-""}
DESKTOPB2G_BRANCH=${DESKTOPB2G_BRANCH:-"master"}
B2G_GAIATEST_TESTVARS=${B2G_GAIATEST_TESTVARS:-"testvars.json"}
B2G_GAIATEST_TYPE=${B2G_GAIATEST_TYPE:-"b2g"}
B2G_GAIATEST_TESTS=${B2G_GAIATEST_TESTS:-"gaiatest/tests/functional/manifest.ini"}

if [[ ${DESKTOPB2G_DIR} == "" ]] || [[ ! -d ${DESKTOPB2G_DIR}/b2g ]]; then
    echo "There is no Desktop B2G under [${DESKTOPB2G_DIR}]! Stop."
    exit 1
else
    echo "DESKTOPB2G_DIR is ${DESKTOPB2G_DIR}"
fi

### Get the absolute path of testvars file
B2G_GAIATEST_TESTVARS_PATH=`readlink -f ${B2G_GAIATEST_TESTVARS}`
if [[ ! -f ${B2G_GAIATEST_TESTVARS_PATH} ]]; then
    echo "No testvars file [${B2G_GAIATEST_TESTVARS_PATH}] for gaia-ui-test."
    exit 1
else
    echo "The testvars file is [${B2G_GAIATEST_TESTVARS_PATH}]."
fi

### Setup user.js for marionette
echo "user_pref('marionette.force-local', true);" >> ${DESKTOPB2G_DIR}/b2g/gaia/profile/user.js

### Checkout the Gaiatest project
if [[ -f common_check_gaia.sh ]]; then
    bash ./common_check_gaia.sh
else
    echo "There is no common_check_gaia.sh scripts."
    exit 1
fi

### change folder into gaia-ui-test
cd gaia/tests/python/gaia-ui-tests/

### remove old files
rm -rf results/

### Using virtual environments
rm -rf .env
virtualenv .env
source .env/bin/activate

### Setup gaiatest
python setup.py develop

### Run gaiatest
echo "Running gaiatest on desktop B2G, type [${B2G_GAIATEST_TYPE}], tests [${B2G_GAIATEST_TESTS}]..."
gaiatest --app=b2gdesktop --binary=${DESKTOPB2G_DIR}/b2g/b2g-bin --profile=${DESKTOPB2G_DIR}/b2g/gaia/profile --testvars=${B2G_GAIATEST_TESTVARS_PATH} --restart --xml-output=results/result.xml --html-output=results/index.html --type=${B2G_GAIATEST_TYPE} ${B2G_GAIATEST_TESTS}

