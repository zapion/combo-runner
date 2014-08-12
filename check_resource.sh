#!/bin/bash

# go to desired folder : /tmp
cd /tmp
TEMP_FOLDER=LOCKS
if [[ ! -d $TEMP_FOLDER ]]; then
    mkdir -p $TEMP_FOLDER
fi
cd $TEMP_FOLDER

# check and create critical section
LOCK_FILE=LOCKED
if [[ -f $LOCK_FILE ]]; then
    COUNTER=1
    while [[ $COUINTER -le 18 ]]
    do
        echo "Another thread is checking resources."
        sleep 10
        if [[ ! -f $LOCK_FILE ]]; then
            touch $LOCK_FILE
            exit 1
        fi
        COUNTER=$COUNTER+1
    done
else
    touch $LOCK_FILE
fi

# critical section (check resources and take it/them)
RESOURCE=EMPTY
DEVICES_LIST=$(adb devices | awk -F" " '(match($1, /^[a-z0-9]/)) {printf "%s ", $1}')
for DEVICE in $DEVICES_LIST; do
    if [[ ! -f $DEVICE ]]; then
        RESOURCE=$DEVICE
        touch $RESOURCE
        break
    fi
done

# keep response in a file so that the
RESULT_FILE=RESULT
if [[ -f $RESULT_FILE ]]; then
    rm -rf $RESULT_FILE
fi
echo "ANDROID_SERIAL=$RESOURCE" > $RESULT_FILE

# release critical section
rm -rf $LOCK_FILE

