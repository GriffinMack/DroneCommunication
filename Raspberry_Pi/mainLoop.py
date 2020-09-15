# Griffin Mack
# 8/29/2020

#
# Main loop to be ran on the Raspberry Pi. Should be started on power up
#
import time

from devices import Drone
from flightControls import decodeMessage, establishGeofence



def promptUserForTestInput():
    message = input("Please enter a command: ")
    return message


def systemStartup():
    # The drone class contains connections to the xbee and the pixhawk
    droneDevice = Drone()
    establishGeofence(droneDevice.pixhawkDevice)
    return droneDevice


def main():
    droneDevice = systemStartup()
    xbeeDevice = droneDevice.getXbeeDevice()
    xbee = xbeeDevice.getXbee()
    while True:
        if xbee:
            # The pollForIncomingMessage is sent the drone device to send heartbeat to the pixhawk
            message = xbeeDevice.pollForIncomingMessage()
            decodeMessage(droneDevice, message)
            # droneDevice.xbeeDevice.sendMessage(returnMessage)
        else:
            message = promptUserForTestInput()
            decodeMessage(droneDevice, message)

if __name__ == "__main__":
    main()
