#!/bin/bash -x

### Create virtual environments
rm -rf .env
virtualenv .env
source .env/bin/activate

### Setup gaiatest
python setup.py develop
if [ "$CUSTOM_GAIA" == "true" ]
  then
  cp -rf /mnt/mtbf_shared/gaia/tests/python/gaia-ui-tests .
  cp -rf /mnt/mtbf_shared/gaia/tests/atoms gaia-ui-tests/gaiatest/
  cd gaia-ui-tests
  python setup.py develop
  cd ..
fi


### Get memory tools
cp -rf /mnt/mtbf_shared/memory_tools/tools/ .
