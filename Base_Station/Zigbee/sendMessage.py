# Griffin Mack
# 8/8/2020
#
# Functions to use the base station XBEE to send messages out to the drone network
#
#

from Zigbee.openBaseStationXBEE import openBaseStationXBEE

def sendMessage(message, droneDevice=None):
    if droneDevice:
        sendDirectMessage(message, droneDevice)
    else:
        sendBroadcastMessage(message)

def sendDirectMessage(message, droneDevice):
    try:
        # take the incoming message and send it out through the base station XBEE to the specified drone
        baseStationXbeeDevice = openBaseStationXBEE()

        print("Sending data to %s >> %s..." %
              (droneDevice.get_64bit_addr(), message))
        baseStationXbeeDevice.send_data(droneDevice, message)
        print("Success")

    finally:
        if baseStationXbeeDevice is not None and baseStationXbeeDevice.is_open():
            baseStationXbeeDevice.close()


def sendBroadcastMessage(message):
    try:
        # take the incoming message and send it out through the base station XBEE to all drones
        baseStationXbeeDevice = openBaseStationXBEE()

        print("Sending data to all devices >> %s..." % (message))
        baseStationXbeeDevice.send_data_broadcast(message)
        print("Success")

    finally:
        if baseStationXbeeDevice is not None and baseStationXbeeDevice.is_open():
            baseStationXbeeDevice.close()
