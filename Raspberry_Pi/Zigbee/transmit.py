from digi.xbee.devices import XBeeDevice
from Zigbee.networkDiscovery import discoverNetwork


def transmit(device, message="received"):
    print(" +--------------------------------------+")
    print(" |      XBee waiting to send data       |")
    print(" +--------------------------------------+\n")
    try:
        device.open()
    except Exception:
        print("device already open")

    try:
        # Obtain the remote XBee device from the XBee network.
        xbee_network = discoverNetwork(device)
        devicesList = xbee_network.get_devices()
        for remote_device in devicesList:
            if remote_device is None:
                print("Could not find the remote device")
                exit(1)

            print("Sending data to %s >> %s..." %
                  (remote_device.get_64bit_addr(), message))

            device.send_data(remote_device, message)

            print("Success")

    finally:
        if device is not None and device.is_open():
            device.close()
