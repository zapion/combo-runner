#!/bin/bash

# stop if no resource fetched
if [ "$ANDROID_SERIAL" = "EMPTY" ]; then 
    echo "No resource fetched."
    exit 1
fi

# generate port number
while true; do
    PORT_OCCUPIED_1=$(adb forward --list | grep "$PORT" -c)
    PORT_OCCUPIED_2=$(netstat -la | grep "$PORT" -c)
    PORT_OCCUPIED=$((PORT_OCCUPIED_1+PORT_OCCUPIED_2))
    if [[ $PORT_OCCUPIED -eq 0 ]]; then
        break
    fi
    PORT=$((PORT+1))
done

RESULT_FILE=PORT_RESULT
echo "PORT=$PORT" > $RESULT_FILE

echo "Port $PORT is selected."
