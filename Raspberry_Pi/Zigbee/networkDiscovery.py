# Griffin Mack
# 8/29/2020

#
# From a drone(with XBEE attached) discover any
# XBEE devices on the same network,
#
# NOTE: This assumes that all xbee devices have been setup correctly with
# seperate identifiers

# imports allowing communication with the xbee
from digi.xbee.models.status import NetworkDiscoveryStatus
from digi.xbee.devices import DigiMeshDevice
import time


def discoverNetwork(droneXbeeDevice):
    print(" +-------------------------------+")
    print(" | DISCOVERING CONNECTED DRONES  |")
    print(" +-------------------------------+\n")

    try:
        droneXbeeDevice.open()
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
        xbeeNetwork = droneXbeeDevice.get_network()
        xbeeNetwork.set_discovery_timeout(5)  # 5 seconds.
        xbeeNetwork.clear()

        xbeeNetwork.add_device_discovered_callback(callback_device_discovered)
        xbeeNetwork.add_discovery_process_finished_callback(
            callback_discovery_finished)

        xbeeNetwork.start_discovery_process()

        print("Discovering remote XBee devices...")
        while xbeeNetwork.is_discovery_running():
            time.sleep(0.1)

        return xbeeNetwork

    except Exception as e:
        print(e)
