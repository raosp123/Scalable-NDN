# Scalable-NDN
Github: https://github.com/raosp123/Scalable-NDN
    !DISCLAIMER! github commits are not indicative of workload done by each member, 100% of the work was done in a single room in the Phoenix labs on campus, with all members contributing to design decisions and taking turns coding


This README is intended to be read from top to bottom, as to prevent the same information being repeated in multiple sections.

0. useful command:

    The best way to ensure ports have been closed, even despite our best efforts to close them in the python code, is to run our `./kill_devices.sh --kill_all` script. Run this if ports are in use after closing the programs

1. Setting up venv

   Install the venv however it is suited to your machine, or follow the steps for linux if needed on the pi
   'https://www.arubacloud.com/tutorial/how-to-create-a-python-virtual-environment-on-ubuntu.aspx'

   Once setup run `pip install requirements.txt` to install necessary dependencies

2. Running Local (Easy)


    1. Getting Files:

    Either cloning the repo mentioned above, or the code bundle provided in the assignment submission

    2. Running:

    Assuming you have the venv setup or manually installed python dependencies, simply running `./start-network-local.sh` will bring up the logger process, the devices incrementally, and then all the sensors.

    You can view all packet routing through the debugger that opens

    After those have been created successfully, you will be presented with user input to simulate you being an actuator connected to device 5. You can search for tags/interests within the network, and if they exist, you will get data back.

    If you exit this loop, you can bring the actuator simulator back up again with `python3 actuator_simulation.py`

    3. Further Tags and node failure:

    If you would like to add your own tags to the system and check for them with the actuator simulator, run `python3 sensor_simple_simulation.py` and similar to the actuator you can infinitely add new tags and their values to the network. You can then query for them again with the actuator simulator

    If you would like to simulate node failure, use the command `./kill_devices.sh --process={process_id}` where process_id is the int id of the device, so (device_1 = 1). Then you can test the behaviour with the actuator simulation again

3. Running on Pi (Hard)


    1. Getting the files on the Pi:

        Git clone or scp code bundle from bb to the pi:

            I'm not sure if instructor users work similarly to undergraduate users, that there is an NFS mounting of the user directory to the Pis. Assuming its the same, this means anything on your macneill user is accessible from your user on the Pi.

            Using Git or scp, get the files onto macneill or the Pi however you are most comfortable

    2. Setting up an SSH TUNNEL:

        Since the raspberry pi does not offer allow us to use our debugging window, we instead use a reverse SSH tunnel to return information back to our logging window. To do this:

        1.  Set up initial tunnel

            If you have access to the trinityVPN, you can ssh directly to the target pi and open up a reverse tunnel using `ssh -R 30303:localhost:30303 user@rasp-XXX.scss.tcd.ie`

            If the vpn is down, you need to do a double hop over the macneill server. First run `ssh -R 30303:localhost:30303 user user@macneill.scss.tcd.ie` before running the second tunnel command above

            This will redirect traffic from port 30303 on the Pi, to 30303 on our local machine, where our logger will be running

            !DISCLAIMER! for tcd undergrad users, it seems ports on macneill are shared across all users. We had an issue where one person was testing the network, while another person had the data appearing in the logger on their local machine.

        2. Run the logger 
        
           run the logger itself on your local machine using `python3 run_logger.py`

        3. Run the network on the Pi

           We experienced an issue where running all 6 sensors for each device while on the Pi causes some issues across the ssh tunnel. Not all packets are being received, and we did not have ample time to debug why. Either the network is too congested, or the Pi does not have enough resources

           So testing locally on the pi goes like this:

           run `./start-network-remote.sh` on the pi to setup the devices, then you have two options to simulate the network:

           1. run `python3 sensor_simple_simulation.py` and publish tags manually to the network

           2. run `python3 actuator_simulation.py` and query for tags manually to the network

        4. Similar to the local testing, you can test network failure further






