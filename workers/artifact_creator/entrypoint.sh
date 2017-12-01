#!/bin/ash

set -x
cd /usr/bin/workers
python3 main.py  --bbb-version 1.3.0b1-build3 --rpi-version 1.3.0b1-build3 --vexpress-version 1.3.0b1-build3
