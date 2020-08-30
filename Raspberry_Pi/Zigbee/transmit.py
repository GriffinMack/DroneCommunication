# Griffin Mack
# 8/29/2020

#
# Transmits a message to either the base station, or all XBEE's in the network
#

from digi.xbee.devices import XBeeDevice
from Zigbee.networkDiscovery import discoverNetwork


def transmitMessage(droneXbeeDevice, message="received"):
    print(" +--------------------------------------+")
    print(" |      XBee waiting to send data       |")
    print(" +--------------------------------------+\n")
    try:
        droneXbeeDevice.open()
    except Exception:
        print("device already open")

    try:
        # Obtain the remote XBee device from the XBee network.
        xbeeNetwork = discoverNetwork(droneXbeeDevice)
        devicesList = xbeeNetwork.get_devices()
        for remoteDevice in devicesList:
            if remoteDevice is None:
                print("Could not find the remote device")
                exit(1)

            print("Sending data to %s >> %s..." %
                  (remoteDevice.get_64bit_addr(), message))

            droneXbeeDevice.send_data(remoteDevice, message)

            print("Success")

    except Exception as e:
        print(e)
