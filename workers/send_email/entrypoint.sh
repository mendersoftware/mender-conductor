#!/bin/sh 

CONDUCTOR=${CONDUCTOR="http://mender-conductor:8080"}

echo "-- conductor API is at ${CONDUCTOR}"

# wait for conductor
tries=0
up=0
while [ "$tries" -lt 20 ]; do
    if ! curl -f "${CONDUCTOR}/api/metadata/taskdefs" > /dev/null 2>&1 ; then
        tries=$((tries + 1))
        echo "-- $(date) waiting for conductor, attempt ${tries}"
        sleep 5
    else
        up=1
        break
    fi
done

if [ "$up" -ne 1 ]; then
    echo "-- max attempts reached, giving up"
    exit 1
fi

python -u /usr/bin/workers/send_email/main.py
exit 1
