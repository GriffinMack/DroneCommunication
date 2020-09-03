# Griffin Mack
# 8/29/2020

#
# Main loop to be ran on the Raspberry Pi. Should be started on power up
#
import time

from devices import localDrone
from flightControls import decodeMessage

def systemStartup():
    droneDevice = localDrone()
    droneDevice.addDataReceivedCallback()
    return droneDevice


def main():
    droneDevice = systemStartup()
    while True:
        message = droneDevice.pollForIncomingMessage()
        decodeMessage(droneDevice, message)



if __name__ == "__main__":
    main()
