# Griffin Mack
# 8/29/2020

#
# Main loop to be ran on the Raspberry Pi. Should be started on power up
#
import time

from devices import Drone
from flightControls import decodeMessage
from collisionAvoidance import establishGeofence


def promptUserForTestInput():
    message = input("Please enter a command: ")
    return message


def systemStartup():
    # The drone class contains connections to the xbee and the pixhawk
    droneDevice = Drone()
    establishGeofence(droneDevice)

    # Add a callback to parse messages received at any time
    # droneDevice.addDataReceivedCallback()

    return droneDevice


def main():
    droneDevice = systemStartup()
    if droneDevice.getXbee():
        while True:
            message = droneDevice.pollForIncomingMessage()
            returnMessage = decodeMessage(droneDevice, message)
            droneDevice.sendMessage(returnMessage)

    else:
        while True:
            message = promptUserForTestInput()
            decodeMessage(droneDevice, message)


if __name__ == "__main__":
    main()
