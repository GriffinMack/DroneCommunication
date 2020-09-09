# DroneCommunication

## Overview
This serves as a repo for our senior design project.

It involves the control of quadcopters under the PX4 firmware and communication with Xbee radio

## Documentation
Documentation on the DRONEKIT python library can be found [here](https://dronekit-python.readthedocs.io/en/latest/guide/vehicle_state_and_parameters.html). This library is instrumental in controlling the pixhawk from the onboard Raspberry Pi.

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
