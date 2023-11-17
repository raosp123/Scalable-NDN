#!/bin/bash

python3 run_logger.py &

sleep 1

#bring up all devices and sensors
echo "bringing up logger process"

for i in $(seq 1 5); do 

echo "starting device${i}"
python3 device${i}_simulation.py &

done

