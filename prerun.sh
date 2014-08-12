#!/bin/bash
echo 'Waiting for device...'

adb reboot
adb wait-for-device

adb shell 'i=1;
retries=60
echo "Waiting for device to boot...";
while [ "$(getprop sys.boot_completed)" == "1" ]; do
  if (( i++ > ($retries - 1) )); then
  	echo "Device failed to boot!";
  	exit 1;
  fi;
  sleep 1;
done'

sleep 45

adb root
sleep 60

### port forward
if [[ -z "$PORT" ]]; then
    adb forward tcp:2828 tcp:2828
else
    adb forward tcp:$PORT tcp:2828
fi

