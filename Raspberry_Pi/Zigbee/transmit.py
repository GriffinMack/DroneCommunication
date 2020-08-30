# Griffin Mack
# 8/29/2020

#
# Transmits a message to either the base station, or all XBEE's in the network
#

from digi.xbee.devices import XBeeDevice
from Zigbee.networkDiscovery import discoverNetwork
from Zigbee.openDroneXBEE import openDroneXBEE

def transmitMessage(droneXbeeDevice, message="received"):
    print(" +--------------------------------------+")
    print(" |      XBee waiting to send data       |")
    print(" +--------------------------------------+\n")
    try:
        droneXbeeDevice.open()
    except Exception:
        print("device already open")

    try:
        print("Sending data to %s >> %s..." %
                ("all devices", message))

        droneXbeeDevice.send_data_broadcast(message)

    except Exception as e:
        print(e)
