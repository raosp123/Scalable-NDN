#!/bin/bash
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





