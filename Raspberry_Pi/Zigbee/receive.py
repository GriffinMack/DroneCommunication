from digi.xbee.devices import XBeeDevice

def receive(device):
    print(" +-----------------------------------------+")
    print(" |      XBee waiting to receive data       |")
    print(" +-----------------------------------------+\n")

    try:

        def data_receive_callback(xbee_message):
            print(xbee_message)
            return xbee_message

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()
