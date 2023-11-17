#!/bin/bash

#bring up all devices and sensors
# command line flag definitions for the parameters mentioned above
while test $# -gt 0; do
	case "$1" in
	--process*)
		PROCESS_NAME=` echo $1 | sed -e 's/^[^=]*=//g'`
		shift
		;;
	
	--kill_all*)
		KILL_ALL="TRUE"
		shift
		;;
		
	*)
		break
		;;
	esac
done	

if [[ ! -z "${PROCESS_NAME}"  ]] ; then

    DEVICE=`ps -ef | grep "[p]ython3 device${PROCESS_NAME}_simulation.py"| awk '{print $2}'`
    
    echo $DEVICE

    echo $DEVICE | while read -r line ; do
    echo "Processing $line"
    kill $line
    done
    # your code goes here
fi

if [[ "${KILL_ALL}" == "TRUE" ]] ; then

    DEVICES=`ps -ef | grep "[p]ython3 device*.*_simulation.py"| awk '{print $2}'`
    
    echo $DEVICES

    echo $DEVICES | while read -r line ; do
    echo "Processing $line"
    kill $line
    done
    # your code goes here

fi




