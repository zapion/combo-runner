#!/bin/bash

GAIA_BRANCH=${GAIA_BRANCH:-"master"}

echo "Checking 'gaia' project..."
if [[ -d ./gaia ]]; then
    echo "Already have gaia folder."
else
    git clone https://github.com/mozilla-b2g/gaia.git
fi
cd gaia/
echo "Checkout Branch [${GAIA_BRANCH}]"
git checkout ${GAIA_BRANCH}
git pull || echo "git pull failed at gaia."
cd ..

