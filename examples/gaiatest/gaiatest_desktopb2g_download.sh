#!/bin/bash

### for other bash script tools call.
case `uname` in
    "Linux"|"CYGWIN"*) SP="=";;
    "Darwin") SP=" ";;
esac

DESKTOPB2G_BRANCH=${DESKTOPB2G_BRANCH:-"master"}
DESKTOPB2G_OS_PLATFORM=${DESKTOPB2G_OS_PLATFORM:-"linux64"}
if [[ ${DESKTOPB2G_BRANCH} -eq "master" ]]; then
    DESKTOPB2G_BRANCH_FLAG="0"
else
    DESKTOPB2G_BRANCH_FLAG=${DESKTOPB2G_BRANCH//"v"/""}
    DESKTOPB2G_BRANCH_FLAG=${DESKTOPB2G_BRANCH_FLAG//"."/""}
fi

echo "Downloading Desktop B2G with Version [${DESKTOPB2G_BRANCH}], platform [${DESKTOPB2G_OS_PLATFORM}]..."

### Checkout the B2G-flash-tool project
if [[ -f common_check_B2G-flash-tool.sh ]]; then
    bash ./common_check_B2G-flash-tool.sh
else
    echo "There is no common_check_B2G-flash-tool.sh scripts."
    exit 1
fi

### Create temp folder
if ! which mktemp > /dev/null; then
    echo "### Package \"mktemp\" not found!"
    rm -rf ./desktopb2g_temp
    mkdir desktopb2g_temp
    cd desktopb2g_temp
    TMP_DIR=`pwd`
    cd ..
else
    rm -rf /tmp/desktopb2g_temp*
    TMP_DIR=`mktemp -d -t desktopb2g_temp.XXXXXXXXXXXX`
fi

### Download B2G desktop client
CUR_DIR=`pwd`
cp -rf ./B2G-flash-tool/. ${TMP_DIR}
cd ${TMP_DIR}
echo "Downloading to ${TMP_DIR}..."
./download_desktop_client.sh --version${SP}${DESKTOPB2G_BRANCH} --os${SP}${DESKTOPB2G_OS_PLATFORM} -d
cd ${CUR_DIR}

source ${TMP_DIR}/B2G_Desktop/${DESKTOPB2G_BRANCH_FLAG}/VERSION-DESKTOP
export DESKTOPB2G_BUILD_ID=${BUILD_ID}
export DESKTOPB2G_BRANCH=${DESKTOPB2G_BRANCH}
export DESKTOPB2G_DIR=${TMP_DIR}/B2G_Desktop/${DESKTOPB2G_BRANCH_FLAG}/${BUILD_ID}/
echo "Desktop B2G: [${DESKTOPB2G_DIR}]"
echo "Build ID is [${BUILD_ID}]"
