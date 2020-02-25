# Griffin Mack
# 12/8/2019

#
# From the base station(laptop with XBEE attached) discover the
# network and grab ititial data
#
# NOTE: This assumes that all xbee devices have been setup correctly with
# seperate identifiers
# NOTE: This also assumes that all devices discovered are running correct
# scripts to return data when given the correct commands

# imports allowing communication with the xbee
from digi.xbee.devices import XBeeDevice
import time


def main():
    try:
        # Define the network modified callback.
        def cb_network_modified(event_type, reason, node):
            print("  >>>> Network event:")
            print("         Type: %s (%d)" % (event_type.description, event_type.code))
            print("         Reason: %s (%d)" % (reason.description, reason.code))

            if not node:
                return

            print("         Node:")
            print("            %s" % node)

        # Callback for discovered devices.
        def callback_device_discovered(remote):
            print("Device discovered: %s" % remote)

        # Callback for discovery finished.
        def callback_discovery_finished(status):
            if status == NetworkDiscoveryStatus.SUCCESS:
                print("Discovery process finished successfully.")
            else:
                print("There was an error discovering devices: %s" % status.description)

        # COM1 should be replaced with whatever port the xbee is attached to
        # usually /dev/tty
        xbee = XBeeDevice("COM1", 9600)

        xbee.open()

        # Get the network.
        xbee_network = xbee.get_network()

        # Configure the discovery options. (allows for easier verification of data)
        xbee_network.set_discovery_options({DiscoveryOptions.APPEND_DD})
        xbee_network.set_discovery_timeout(25)

        xbee_network.add_device_discovered_callback(callback_device_discovered)
        xbee_network.add_discovery_process_finished_callback(
            callback_discovery_finished
        )
        xbee_network.add_network_modified_callback(cb_network_modified)

        # Begin discovering all devices on the network, and give time to finish
        xbee_network.start_discovery_process()
        while xbee_network.is_discovery_running():
            time.sleep(0.2)

        # Get a list of the devices added to the network.
        devices = xbee_network.get_devices()
        print(devices)

        # start to send commands to connected devices
    finally:
        if xbee is not None and xbee.is_open():
            xbee.close()


if __name__ == "__main__":
    main()
