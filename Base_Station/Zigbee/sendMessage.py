# Griffin Mack
# 8/8/2020
#
# Functions to use the base station XBEE to send messages out to the drone network
#
#

from Zigbee.openBaseStationXBEE import openBaseStationXBEE


def sendMessage(message, droneDevice, baseStationXbeeDevice):
    if droneDevice:
        sendDirectMessage(message, droneDevice, baseStationXbeeDevice)
    else:
        sendBroadcastMessage(message, baseStationXbeeDevice)


def sendDirectMessage(message, droneDevice, baseStationXbeeDevice):
    try:
        print("Sending data to %s >> %s..." %
              (droneDevice.get_64bit_addr(), message))
        baseStationXbeeDevice.send_data(droneDevice, message)
        print("Success")

    finally:
        if baseStationXbeeDevice is not None and baseStationXbeeDevice.is_open():
            # baseStationXbeeDevice.close()
            pass


def sendBroadcastMessage(message, baseStationXbeeDevice):
    try:

        print("Sending data to all devices >> %s..." % (message))
        baseStationXbeeDevice.send_data_broadcast(message)
        print("Success")

    finally:
        if baseStationXbeeDevice is not None and baseStationXbeeDevice.is_open():
            # baseStationXbeeDevice.close()
            pass
