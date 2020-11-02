from Devices.Pixhawk import PixhawkDevice
from Devices.Xbee import XbeeDevice


"""
A class used to represent a drone, which is attached to an XBEE device, Pixhawk device, and a ZUBAX device.
...

Attributes
----------
Methods
-------
"""


class Drone(PixhawkDevice, XbeeDevice):
    macAddressDictionary = {
        "0013A20041C6B692": "Bravo",
        "0013A20041C6B69C": "Charlie",
        "0013A2004195CF95": "Base Station",
        "0013A2004192DBC0": "Stanley",
        "9999": "No Zigbee Attached",
    }

    def __init__(self):
        XbeeDevice.__init__(self)
        PixhawkDevice.__init__(self)
        self.droneHumanName = self.macAddressDictionary[self.macAddress]
        self.safeDistance = 2  # meters
        self.safeAltitude = 2  # meters

        # Useful variables that are updated frequently
        self.currentPosition = None

    def getDroneHumanName(self):
        return self.droneHumanName

    def getSafeDistance(self):
        return self.safeDistance

    def getSafeAltitude(self):
        return self.safeAltitude

    def getCurrentPosition(self):
        return self.currentPosition

    def setCurrentPosition(self, position):
        self.currentPosition = position

    def addDataReceivedCallback(self):
        # This is only in this class because the data callback may need info only Drone has
        def data_receive_callback(xbee_message):
            print(
                "\nFrom %s >> %s"
                % (
                    xbee_message.remote_device.get_64bit_addr(),
                    xbee_message.data.decode(),
                )
            )

        self.xbee.add_data_received_callback(data_receive_callback)