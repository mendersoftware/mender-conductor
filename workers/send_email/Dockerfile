FROM python:2.7.14-alpine3.7

RUN apk update && apk add \
    git \
    curl 

RUN git clone https://github.com/Netflix/conductor.git && \
    cd conductor/client/python && \
    git checkout v1.8.9

RUN pip install conductor/client/python
RUN pip install configargparse

RUN mkdir /usr/bin/workers
COPY worker /usr/bin/workers/send_email

COPY entrypoint.sh /usr/bin/entrypoint.sh

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
