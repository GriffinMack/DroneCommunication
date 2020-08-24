# DroneCommunication 
This serves as a repo of our software demos for our senior design project.

It involves the control of quadcopters under the PX4 firmware and communication with Xbee radio

Documentation on the DRONEKIT python library can be found below. This library is instrumental in controlling the pixhawk from the onboard Raspberry Pi.
https://dronekit-python.readthedocs.io/en/latest/guide/vehicle_state_and_parameters.html

To be ran on Python 2.7 or 3.8 on the onboard Raspberry Pi 3B+. Reference user manual for setup instructions

Setup Instructions:

1.Make sure your machine is running a linux environment and has python 3.8 installed
2.Install the required pip packages using 'pip install -r requirements.txt'
3.If working on Zigbee devices, make sure to find what ports your xbee's are connected to locally. The command 'ls /dev/{tty,cu}.*' is useful for this. Personally, my XBEE was found under /dev/tty.usbserial-0001