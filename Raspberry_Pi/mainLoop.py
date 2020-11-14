# Griffin Mack
# 8/29/2020

#
# Main loop to be ran on the Raspberry Pi. Should be started on power up
#
import time

from devices import Drone
from flightControls import (
    establishGeofence,
    calibrateDevice,
    getDroneCoordinates,
    decodeMessage,
    statusText,
)


def promptUserForTestInput():
    message = input("Please enter a command: ")
    return message


def systemStartup():
    # The drone class contains connections to the xbee and the pixhawk
    droneDevice = Drone()
    # Establish a default geofence
    # establishGeofence(droneDevice)
    # Calibrate any sensors
    # calibrateDevice(droneDevice)
    statusText(droneDevice)
    # Add a callback to parse messages received at any time
    # droneDevice.addDataReceivedCallback()

    return droneDevice


def main():
    droneDevice = systemStartup()
    if droneDevice.getXbee():
        while True:
            print("-- Waiting for a message..")
            message, sender = droneDevice.pollForIncomingMessage()
            if message:
                returnMessage = decodeMessage(droneDevice, message)
                if returnMessage:
                    droneDevice.sendMessage(returnMessage, sender)
            # droneDevice.sendMessage(getDroneCoordinates(droneDevice))

    else:
        while True:
            message = promptUserForTestInput()
            decodeMessage(droneDevice, message)


if __name__ == "__main__":
    main()
