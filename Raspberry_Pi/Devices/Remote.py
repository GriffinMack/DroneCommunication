
"""
A class used to represent a device that is connected to the drone via a remote connection. This device could be a drone or a base station
...

Attributes
----------
remoteXbee : digimesh xbee remote device
    Contains useful info/methods. See Xbee python library for more info
macAddress : str
    The mac address of the xbee connected to the remote device. Can be found under the xbee device hardware
remoteDeviceHumanName : str
    Friendlier names for the drones/Base station so we don't have to talk about them with their mac addresses

Methods
-------
classifyRemoteDevice(classification)
    classifies if the remote device is a base station or a drone. "base station" or "drone" string
"""


class remoteDevice:
    def __init__(self, remoteXbeeDevice, classification=None):
        self.remoteXbee = remoteXbeeDevice
        self.macAddress = str(remoteXbee.get_64bit_addr())
        self.remoteDeviceHumanName = macAddressDictionary[self.macAddress]
        # we dont know if this device is a drone or the base station
        self.classification = classification

    def classifyRemoteDevice(self, classification):
        self.classification = classification