# DroneCommunication

## Overview
This serves as a repo for our Dr. Hu's Drone Communication senior design project.

It involves the control of quadcopters under the PX4 firmware and communication with Xbee radio. Two software stacks are contained here: base station and raspberry pi. Both stacks are essential for the control of our drone swarms. See the individual folder readme's for more information.

## Documentation
Documentation on the MavSDK can be found on the github [here](https://github.com/mavlink/MAVSDK). MavSDK is used to simulate the drone behavior in a SITL (system in the loop) environment prior to physical testing.

Documentation on the XBEE python library can be found [here](https://xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html). This library is used to facilitate communication between Ground Control Software and the drone's onboard computers.

To be ran on Python 2.7 or 3.8 on the onboard Raspberry Pi 3B+. Reference our [user manual](https://drive.google.com/drive/u/0/folders/1BpD5cyexIqJkpC1YarY-sfYrys9aw6gL) for setup instructions



## Installation
Before continuing, make sure your system is running a linux environment and has Python 3.X installed

Install the required pip packages for this project 
```
pip3 install -r requirements.txt
````
If working on Zigbee devices, make sure to find what ports your xbee's are connected to locally. Usually the port will look something like /dev/tty.usbserial-0001
```
ls /dev/{tty,cu}.*
```
