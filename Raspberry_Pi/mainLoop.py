# Griffin Mack
# 8/29/2020

#
# Main loop to be ran on the Raspberry Pi. Should be started on power up
#
import time

from devices import drone
from flightControls import decodeMessage

def promptUserForTestInput():
    message = input("Please enter a command: ")
    return message


def systemStartup():
    # The drone class contains connections to the xbee and the pixhawk
    droneDevice = drone()

    # droneDevice.addDataReceivedCallback()
    return droneDevice


def main():
    droneDevice = systemStartup()
    while True:
        if droneDevice.xbeeDevice.localXbee:
            # The pollForIncomingMessage is sent the drone device to send heartbeat to the pixhawk
            message = droneDevice.xbeeDevice.pollForIncomingMessage()
            returnMessage = decodeMessage(droneDevice, message)
            droneDevice.xbeeDevice.sendMessage(returnMessage)
        else:
            returnMessage = promptUserForTestInput()
            returnMessage = decodeMessage(droneDevice, returnMessage)
        print(returnMessage)



if __name__ == "__main__":
    main()
