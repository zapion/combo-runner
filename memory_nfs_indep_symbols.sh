#!/bin/bash -x
hostname
pwd

### ZIP all the memory report files
if [ -e about-memory.zip ];then
   echo "Removing Old Memory Report Files"
   rm -f about-memory.zip
fi

cd mtbf_driver
echo "Creating all-about-memory Folder"
mkdir -p all-about-memory
if [ -e about-memory-0 ];then
   echo "Moving All The Memory Status Files"
   mv about-memory-* all-about-memory
fi

echo "Ziping All The Memory Status File And Removing Folders"
zip -r -9 -u about-memory.zip all-about-memory
rm -rf about-memory-*
rm -rf all-about-memory

pwd
ls

mkdir -p ${BUILD_NUMBER}.output

### get all the crash reports without parsing the symbols
cd ${BUILD_NUMBER}.output
adb pull /data/b2g/mozilla/Crash\ Reports/pending/ . || echo 0
adb pull /data/b2g/mozilla/Crash\ Reports/submitted/ . || echo 0
cd ..

### check if we need to kill to get minidump
if [ -z "$GET_MINIDUMP" ] || [ 'true' == $GET_MINIDUMP ];then
    cd $BUILD_NUMBER.output
    rm *.dmp
    ### kill b2g to get its crash report
    echo "Killing B2G For Getting DMP Files"
    B2G_PID=$(adb shell b2g-ps | grep b2g -m 1 | awk -F" " '{print $3}')
    echo "B2G pid: $B2G_PID"
    adb shell kill -11 $B2G_PID

    sleep 30
    adb pull /data/b2g/mozilla/Crash\ Reports/pending/ . || echo 0
    
    unzip $WORKSPACE/symbols-$BUILD_NUMBER.zip -d symbols/
    ### get minidump from minidump_stackwalk
    cp /mnt/mtbf_shared/memory_tools/minidump_stackwalk .

    for dmpfile in *.dmp
    do
        #adb shell rm /data/b2g/mozilla/Crash\ Reports/pending/$dmpfile
        ./minidump_stackwalk $dmpfile symbols/ > minidmp_result_$dmpfile.txt
    done

    rm -rf symbols/

    cd ..
fi

echo "now achiving files."
# clean up old zipped files and zipped the new results
zip -r -9 -u output_debug_${BUILD_NUMBER}.zip ${BUILD_NUMBER}.output
rm -rf $BUILD_NUMBER.output

exit $EXIT_STAT
