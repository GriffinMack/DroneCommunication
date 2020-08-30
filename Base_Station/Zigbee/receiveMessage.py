from Zigbee.openBaseStationXBEE import openBaseStationXBEE


def pollForIncomingMessage(baseStationXbeeDevice):
    print(" +-----------------------------------------+")
    print(" |      XBee waiting to receive data       |")
    print(" +-----------------------------------------+\n")

    try:
        print("Waiting for data...\n")
        messageReceived = False
        while not messageReceived:
            xbeeMessage = baseStationXbeeDevice.read_data()
            if xbeeMessage is not None:
                messageReceived = True
                print("From %s >> %s" % (xbeeMessage.remote_device.get_64bit_addr(),
                                         xbeeMessage.data.decode()))
                remoteDevice = xbeeMessage.remote_device
                incomingData = xbeeMessage.data
                isBroadcast = xbeeMessage.is_broadcast
                messageTimestamp = xbeeMessage.timestamp
        return incomingData.decode()
    except Exception as e:
        print(e)