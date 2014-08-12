#!/bin/bash -x

### reset device memory
adb reboot-bootloader
sleep 20
fastboot -s ${ANDROID_SERIAL} oem mem 0
fastboot reboot
adb wait-for-device

### copy files from mount drive
cp /mnt/mtbf_shared/$DEVICE_VERSION/symbols.zip symbols.zip
mv symbols.zip symbols-$BUILD_NUMBER.zip

### default to flash the phone
if [ -z "$FLASH_PHONE" ] || [ "$FLASH_PHONE" == "true" ]; then
    ### get shallow flash script and all related build files
    cp /mnt/mtbf_shared/shallow_flash.sh .
    cp /mnt/mtbf_shared/$DEVICE_VERSION/* .

    ### shallow flash the build
    pwd
    ./shallow_flash.sh --gaia=gaia.zip --gecko=b2g.tar.gz -y
    rm -rf gaia.zip b2g.tar.gz
    cat BuildID
fi
