FROM python:2.7.14-alpine3.7

COPY patches /patches
COPY worker /usr/bin/workers/send_email

RUN apk update && \
    apk add --no-cache git && \
    git clone https://github.com/Netflix/conductor.git && \
    cd /conductor && \
    git checkout v2.12.4 && \
    for file in $(ls -1 /patches/); do git apply /patches/$file; done && \
    pip install --no-cache-dir --disable-pip-version-check /conductor/client/python && \
    pip install --no-cache-dir --disable-pip-version-check configargparse && \
    rm -rf /conductor && \
    rm -rf /patches && \
    apk del git

CMD ["/usr/local/bin/python2.7", "-u", "/usr/bin/workers/send_email/main.py"]
