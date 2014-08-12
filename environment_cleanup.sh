#!/bin/bash -x

# release resource after finished mtbf
# originally generated from check_resource.sh
rm /tmp/LOCKS/$ANDROID_SERIAL

# release the port used
# originally generated from port_detection.sh
if [[ -z "$PORT" ]]; then
    adb forward --remove tcp:2828
else
    adb forward --remove tcp:$PORT
fi
