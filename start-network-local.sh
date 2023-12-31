#!/bin/bash

mkdir -p foo

echo "bringing up logger process"

python3 run_logger.py &

sleep 8

#bring up all devices and sensors

for i in $(seq 1 5); do 

echo "starting device${i}"
python3 device${i}_simulation.py &
sleep 1

done

echo "starting dust sensors"
python3 dust_sensor_simulation.py &

sleep 2

echo "starting temperature sensors" 
python3 temp_sensor_simulation.py &

sleep 2

echo "starting wind_sensors"
python3 wind_sensor_simulation.py &

sleep 2

echo "starting soil_humidty sensors"
python3 soil_moisture_sensor_simulation.py &

sleep 2

echo "starting gas sensors"
python3 gas_sensor_simulation.py &

sleep 2

echo "starting light sensor"
python3 light_sensor_simulation.py &

sleep 2

python3 actuator_simulation.py