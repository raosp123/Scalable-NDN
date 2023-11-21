

echo "bringing up logger process"

#bring up all devices and sensors

mkdir -p keys

for i in $(seq 1 5); do 

echo "starting device${i}"
python3 device${i}_simulation.py &
sleep 1

done

