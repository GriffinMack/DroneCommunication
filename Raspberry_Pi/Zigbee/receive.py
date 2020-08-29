from digi.xbee.devices import XBeeDevice


def receive(droneXbeeDevice):
    print(" +-----------------------------------------+")
    print(" |      XBee waiting to receive data       |")
    print(" +-----------------------------------------+\n")
    try:
        droneXbeeDevice.open()
    except Exception:
        print("XBEE device already open")

    try:
        def data_receive_callback(xbee_message):
            print(xbee_message.data.decode())

        droneXbeeDevice.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    except Exception as e:
        print(e)
