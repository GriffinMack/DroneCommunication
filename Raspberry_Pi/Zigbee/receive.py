# Griffin Mack
# 8/29/2020

#
# Waits for a message from another device in the drone's XBEE network
#

from digi.xbee.devices import XBeeDevice


def receiveMessage(droneXbeeDevice):
    print(" +-----------------------------------------+")
    print(" |      XBee waiting to receive data       |")
    print(" +-----------------------------------------+\n")
    try:
        droneXbeeDevice.open()
    except Exception:
        print("XBEE device already open")

    try:
        def data_receive_callback(xbeeMessage):
            # TODO: Call flight controls based on the xbeeMessage received
            print(xbeeMessage.data.decode())

        droneXbeeDevice.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    except Exception as e:
        print(e)
