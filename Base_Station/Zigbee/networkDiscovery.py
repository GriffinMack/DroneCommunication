# Griffin Mack
# 12/8/2019

#
# From the base station(laptop with XBEE attached) discover any
# XBEE devices on the same network, and rename the devices appropriately
#
# NOTE: This assumes that all xbee devices have been setup correctly with
# seperate identifiers

# imports allowing communication with the xbee
from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import DigiMeshDevice
import time

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/tty.usbserial-0001"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600
# TODO: use this drone dictionary to tell which XBEE's are possibly in the network. Use the mac address on the XBEE





def discoverNetwork(device):
    print(" +-------------------------------+")
    print(" | DISCOVERING CONNECTED DRONES  |")
    print(" +-------------------------------+\n")

    try:
        device.open()
    except Exception:
        print("device already open")

    try:
        # Callback for discovered devices.
        def callback_device_discovered(remote):
            print("Device discovered: %s" % remote)

        # Callback for discovery finished.
        def callback_discovery_finished(status):
            if status == NetworkDiscoveryStatus.SUCCESS:
                print("Discovery process finished successfully.")
            else:
                print("There was an error discovering devices: %s" %
                      status.description)
        xbee_network = device.get_network()
        xbee_network.set_discovery_timeout(5)  # 5 seconds.
        xbee_network.clear()

        xbee_network.add_device_discovered_callback(callback_device_discovered)
        xbee_network.add_discovery_process_finished_callback(
            callback_discovery_finished)

        xbee_network.start_discovery_process()

        print("Discovering remote XBee devices...")
        while xbee_network.is_discovery_running():
            time.sleep(0.1)

        return xbee_network

    except Exception as e:
        print(e)
