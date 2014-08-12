#!/bin/bash -x

### Enter virtual environment
source .env-$BUILD_NUMBER/bin/activate

cd mtbf_driver

### May need to make environmental variables for testvars file
if [[ -z "$ANDROID_SERIAL" ]]; then
    cp $TESTVAR testvars.json
else
    cp /mnt/mtbf_shared/testvars/testvars_$ANDROID_SERIAL.json testvars.json
fi

### Create conf for different location
 sed s/\"archive\":\ \"/\"archive\":\ \"$BUILD_NUMBER./g $CONF_LOCATION > $CONF_LOCATION.$BUILD_NUMBER

### May need to make environmental variables for options
if [[ -z "$PORT" ]]; then
    FILTER=$(MOZ_IGNORE_NUWA_PROCESS=true MTBF_TIME=$MTBF_TIME MTBF_CONF=$CONF_LOCATION.$BUILD_NUMBER mtbf --address=localhost:2828 --testvars=testvars.json $TEST_TORUN)
else
    FILTER=$(MOZ_IGNORE_NUWA_PROCESS=true MTBF_TIME=$MTBF_TIME MTBF_CONF=$CONF_LOCATION.$BUILD_NUMBER mtbf --address=localhost:$PORT --testvars=testvars.json $TEST_TORUN)
fi

echo "EXIT_STAT=$?" > temp_env
