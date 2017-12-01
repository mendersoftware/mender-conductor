FROM alpine:3.4

RUN apk update && apk add \
    python3 \
    git \
    parted \
    e2fsprogs-extra

RUN git clone https://github.com/Netflix/conductor.git && \
    cd conductor/client/python && \
    git checkout v1.8.1

RUN pip3 install conductor/client/python
RUN pip3 install configargparse
RUN pip3 install boto3

COPY . /usr/bin/workers/
COPY entrypoint.sh /usr/bin/entrypoint.sh

# ADD IMAGES
RUN mkdir -p /usr/bin/workers/images/rpi3/1.3.0b1-build3
RUN mkdir -p /usr/bin/workers/images/bbb/1.3.0b1-build3
RUN mkdir -p /usr/bin/workers/images/vexpress-qemu/1.3.0b1-build3

# BBB images
ADD https://s3.amazonaws.com/mender/1.3.0b1-build3/beaglebone/beaglebone_release_1_1.3.0b1-build3.mender /usr/bin/workers/images/bbb/1.3.0b1-build3/
ADD https://s3.amazonaws.com/mender/1.3.0b1-build3/beaglebone/beaglebone_release_2_1.3.0b1-build3.mender /usr/bin/workers/images/bbb/1.3.0b1-build3/
ADD https://s3.amazonaws.com/mender/1.3.0b1-build3/beaglebone/mender-beaglebone_1.3.0b1-build3.sdimg.gz /usr/bin/workers/images/bbb/1.3.0b1-build3/
RUN gunzip /usr/bin/workers/images/bbb/1.3.0b1-build3/mender-beaglebone_1.3.0b1-build3.sdimg.gz 
 
# RPI3 images
ADD https://s3.amazonaws.com/mender/1.3.0b1-build3/raspberrypi3/raspberrypi3_release_1_1.3.0b1-build3.mender /usr/bin/workers/images/rpi3/1.3.0b1-build3/
ADD https://s3.amazonaws.com/mender/1.3.0b1-build3/raspberrypi3/raspberrypi3_release_2_1.3.0b1-build3.mender /usr/bin/workers/images/rpi3/1.3.0b1-build3/
ADD https://s3.amazonaws.com/mender/1.3.0b1-build3/raspberrypi3/mender-raspberrypi3_1.3.0b1-build3.sdimg.gz /usr/bin/workers/images/rpi3/1.3.0b1-build3/
RUN gunzip /usr/bin/workers/images/rpi3/1.3.0b1-build3/mender-raspberrypi3_1.3.0b1-build3.sdimg.gz

# VEXPRESS-QEMU images
ADD https://s3.amazonaws.com/mender/1.3.0b1-build3/vexpress-qemu/vexpress_release_1_1.3.0b1-build3.mender /usr/bin/workers/images/vexpress-qemu/1.3.0b1-build3/
ADD https://s3.amazonaws.com/mender/1.3.0b1-build3/vexpress-qemu/vexpress_release_2_1.3.0b1-build3.mender /usr/bin/workers/images/vexpress-qemu/1.3.0b1-build3/

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
