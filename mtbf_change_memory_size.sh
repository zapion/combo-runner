#!/bin/bash -x
# set variable for checking
if [[ ${MEMORYSIZE} -eq 0 ]]; then
    CMPSTR=auto
else
    CMPSTR=${MEMORYSIZE}m
fi

# reboot to fastboot mode and change the memory size3
adb reboot-bootloader
sleep 20
fastboot -s ${ANDROID_SERIAL} oem mem ${MEMORYSIZE}

# check if the memory size is right
MACHINESIZE=$(fastboot getvar mem 2>&1 | grep mem | awk '{print $2}')
if [[ $MACHINESIZE = $CMPSTR ]]; then
    echo "Memory size set okay." 
else
    echo "There are some issue setting the memory size."
    exit 1
fi

# reboot and wait for device to come back
fastboot reboot
adb wait-for-device
sleep 10
adb reboot
adb wait-for-device

/mnt/mtbf_shared/B2G-flash-tool/enable_certified_apps_for_devtools.sh
