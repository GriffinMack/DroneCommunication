# Griffin Mack
# 8/29/2020

#
# Main loop to be ran on the Raspberry Pi. Should be started on power up
#

from Zigbee.openDroneXBEE import openDroneXBEE
from Zigbee.receive import receiveMessage
from Zigbee.transmit import transmitMessage


def systemStartup():
    droneDevice = openDroneXBEE()
    return droneDevice


def main():
    droneDevice = systemStartup()

    while True:
        # Wait for a communication from the XBEE
        receiveMessage(droneDevice)
        xbeeMessage = "success"
        transmitMessage(droneDevice, xbeeMessage)


if __name__ == "__main__":
    main()
