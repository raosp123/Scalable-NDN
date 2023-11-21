#!/bin/bash

echo "bringing up logger process"

#bring up all devices and sensors

echo "ensure the ssh tunnel is running correctly, to check ports are listening run 'ss -ltu | grep 30303'"

mkdir -p keys

python3 devices.py &
