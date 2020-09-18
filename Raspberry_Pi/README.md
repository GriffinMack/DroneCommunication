## Multi-Drone Simulation
Build PX4
```
make px4_sitl_default
```
Run sitl_multiple_run.sh, specifying the number of instances to start (e.g. 2):
```
./Tools/sitl_multiple_run.sh 2
```
Start the first instance:
```
./Tools/jmavsim_run.sh -l
```
Start subsequent instances, specifying the simulation TCP port for the instance:
```
./Tools/jmavsim_run.sh -p 4561 -l
```
The port should be set to 4560+i for i in [0, N-1].
Developer APIs such as Dronecode SDK or MAVROS connect on the UDP port 14540 (first instance), UDP port 14541 (second instance), and so on.

Copy Raspberry_Pi folder and paste into the main directory

In devices.py:
```
change drone.connect(system_address="udp://:14540") to drone.connect(system_address="udp://:14541")

change for port, desc, _ in sorted(openPortsList, reverse=True): to for port, desc, _ in sorted(openPortsList):
```
