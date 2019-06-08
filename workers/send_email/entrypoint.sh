#!/bin/sh 

CONDUCTOR=${CONDUCTOR="http://mender-conductor:8080"}

ts() {
    echo -ne "[$(python -c "from datetime import datetime; now=datetime.now(); string_i_want=('%04d-%02d-%02d %02d:%02d:%02d,%03d'%(now.year,now.month,now.day,now.hour,now.minute,now.second,now.microsecond))[:-3]; print( string_i_want )")]"
}

echo "$(ts) [INFO    ] conductor API is at ${CONDUCTOR}"

# wait for conductor
tries=0
up=0
while [ "$tries" -lt 20 ]; do
    if ! curl -f "${CONDUCTOR}/api/metadata/taskdefs" > /dev/null 2>&1 ; then
        tries=$((tries + 1))
        echo "$(ts) [INFO    ] waiting for conductor, attempt ${tries}"
        sleep 5
    else
        up=1
        break
    fi
done

if [ "$up" -ne 1 ]; then
    echo "$(ts) [ERROR   ] max attempts reached, giving up"
    exit 1
fi

/usr/local/bin/python2.7 -u /usr/bin/workers/send_email/main.py
exit 1
