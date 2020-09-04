from digi.xbee.devices import DigiMeshDevice
import serial.tools.list_ports
from digi.xbee.models.status import NetworkDiscoveryStatus

from dronekit import connect, VehicleMode, LocationGlobalRelative

import time

"""
droneDictionary : dictionary
    HARD CODED!! Contains the names of all the drones we have available relative to their mac address
    TODO: Make this dictionary available to all areas of the project in one location
"""
macAddressDictionary = {
    "0013A20041C6B692": "Griffin's test drone",
    "0013A20041C6B69C": "Griffin's base station",
    "0000": "Stanley",
    "0001": "Charlie",
    "0002": "Bravo",
    "9999": "No Zigbee Attached"
}
"""
A class used to represent a drone, which is attached to an XBEE device, Pixhawk device, and a ZUBAX device.
...

Attributes
----------
Methods
-------
"""


class drone:
    def __init__(self):
        self.xbeeDevice = localXbeeDevice()
        self.droneHumanName = macAddressDictionary[self.xbeeDevice.macAddress]
        self.pixhawkDevice = localPixhawkDevice()


"""
A class used to represent a pixhawk.
...

Attributes
----------
Methods
-------
"""


class localPixhawkDevice:
    def __init__(self):
        self.sitl = None
        self.pixhawkVehicle = self.connectToVehicle()
    def connectToVehicle(self):
        # TODO: Connect to the correct USB device connected to the Pixhawk

        # Start SITL if no pixhawk device is found
        import dronekit_sitl
        self.sitl = dronekit_sitl.start_default()
        connection_string = self.sitl.connection_string()
        print('Connecting to vehicle on: %s' % connection_string)
        self.pixhawkVehicle = connect(
            connection_string, wait_ready=True, timeout=30, heartbeat_timeout=30)
        return self.pixhawkVehicle
#
# Private Functions
# -----------------
#


"""
A class used to represent a pixhawk.
...

Attributes
----------
Methods
-------
"""


"""
A class used to represent the xbee device, which is attached to a drone.
...

Attributes
----------
localXbeeDevice : <class 'digi.xbee.devices.DigiMeshDevice'>
    Contains useful info/methods. See Xbee python library for more info
macAddress : str
    The mac address of the xbee connected to the drone. Can be found under the xbee device hardware
droneHumanName : str
    A human readable name for the drone xbee device
remoteDeviceList : List[remoteDrone]
    A list of all the remote drones currently found in the network. Could be drones or the base station
xbeeNetwork : xbeeNetwork object
    Contains useful info/methods about the discovered xbee network. See Xbee python library for more info
Methods
-------
openDroneXbee()
    checks all raspi serial ports and finds the one with an Xbee plugged into it. returns the opened device
discoverNetwork()
    gets and returns the network that is attached to the local xbee device ("getting the network" involves discovering all remote devices that have the same NodeID as the local xbee device).
sendMessage(message, remoteDevice=None)
    sends out the inputted message. Depending on if a remoteDevice is specified, the message will either be direct or a broadcast
pollForIncomingMessage()
    blocking function that waits for a message. Returns the data contained in the message once received
addDataReceivedCallback()
    add the option for the base station to accept messages it didn't request. Add to this function if you want functionality based on the incoming message
closeDroneXbeeDevice()
    closes the serial connection to the base station xbee
"""


class localXbeeDevice:
    def __init__(self):
        self.localXbeeDevice = self.openDroneXbee()
        self.remoteDeviceList = []  # the discover network script will fill this in
        # TODO: Remove this check. Only to allow CLI development with no Xbee hardware
        try:
            self.macAddress = str(self.localXbeeDevice.get_64bit_addr())
        except AttributeError:
            self.macAddress = "9999"
            self.remoteDeviceList = ["9999"]
        # we dont need the network until we want to send a direct message
        self.xbeeNetwork = None

    def openDroneXbee(self):
        serialPorts = self.__findOpenSerialPorts()
        for port in serialPorts:
            try:
                device = DigiMeshDevice(port, 9600)
                device.open()
                return device
            except Exception:
                pass
        return None

    def discoverNetwork(self):
        print(" +-------------------------------+")
        print(" | DISCOVERING CONNECTED DRONES  |")
        print(" +-------------------------------+\n")

        try:
            self.localXbeeDevice.open()
        except Exception:
            pass

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
            self.xbeeNetwork = self.localXbeeDevice.get_network()
            self.xbeeNetwork.set_discovery_timeout(5)  # 5 seconds.
            self.xbeeNetwork.clear()

            self.xbeeNetwork.add_device_discovered_callback(
                callback_device_discovered)
            self.xbeeNetwork.add_discovery_process_finished_callback(
                callback_discovery_finished)

            self.xbeeNetwork.start_discovery_process()

            print("Discovering remote XBee devices...")
            while self.xbeeNetwork.is_discovery_running():
                time.sleep(0.1)
            self.__repopulateRemoteDeviceList()  # update the remote drone list
            return self.xbeeNetwork

        except Exception as e:
            print(e)

    def sendMessage(self, message, remoteDevice=None):
        # TODO: Remove this check. Only to allow CLI development with no Xbee hardware
        if self.localXbeeDevice is None:
            print(f"sending message: {message}")
        elif remoteDevice:
            self.__sendDirectMessage(message, remoteDevice)
        else:
            self.__sendBroadcastMessage(message)

    def pollForIncomingMessage(self):
        print(" +-----------------------------------------+")
        print(" |      XBee waiting to receive data       |")
        print(" +-----------------------------------------+\n")

        try:
            messageReceived = False
            while not messageReceived:
                xbeeMessage = self.localXbeeDevice.read_data()
                if xbeeMessage is not None:
                    messageReceived = True
                    print("From %s >> %s" % (xbeeMessage.remote_device.get_64bit_addr(),
                                             xbeeMessage.data.decode()))
            return xbeeMessage.data.decode()
        except Exception as e:
            print(e)

    def addDataReceivedCallback(self):
        def data_receive_callback(xbee_message):
            print("\nFrom %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                       xbee_message.data.decode()))
        self.localXbeeDevice.add_data_received_callback(data_receive_callback)

    def closeDroneXbeeDevice(self):
        if self.localXbeeDevice is not None and self.localXbeeDevice.is_open():
            self.localXbeeDevice.close()

#
# Private Functions
# -----------------
#
    def __sendDirectMessage(self, message, remoteDevice):
        # sends a message directly to the specified droneDevice
        try:
            print("Sending data to %s >> %s..." %
                  (remoteDevice.remoteXbeeDevice.get_64bit_addr(), message))
            self.localXbeeDevice.send_data(
                remoteDevice.remoteXbeeDevice, message)
            print("Success")

        finally:
            if self.localXbeeDevice is not None and self.localXbeeDevice.is_open():
                # self.localXbeeDevice.close()
                pass

    def __sendBroadcastMessage(self, message):
        # sends a message to all drones in the network
        try:

            print("Sending data to all devices >> %s..." % (message))
            self.localXbeeDevice.send_data_broadcast(message)
            print("Success")

        finally:
            if self.localXbeeDevice is not None and self.localXbeeDevice.is_open():
                # self.localXbeeDevice.close()
                pass

    def __findOpenSerialPorts(self):
        # Grabs all open serial ports
        openPortsList = serial.tools.list_ports.comports()
        serialPorts = []
        # reverse allows multiple xbee's to be opened on a PC
        for port, desc, _ in sorted(openPortsList, reverse=True):
            if desc != "n/a":
                serialPorts.append(port)
        return serialPorts

    def __repopulateRemoteDeviceList(self):
        # Clears the drone list and repopulates it based on the current xbeeNetwork
        self.remoteDeviceList.clear()
        for remoteDevice in self.xbeeNetwork.get_devices():
            newRemoteDrone = remoteDevice(remoteDevice)
            self.remoteDeviceList.append(newRemoteDrone)


"""
A class used to represent a device that is connected to the drone via a remote connection. This device could be a drone or a base station
...

Attributes
----------
remoteXbeeDevice : digimesh xbee remote device
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

    def __init__(self, remoteXbeeDevice):
        self.remoteXbeeDevice = remoteXbeeDevice
        self.macAddress = str(remoteXbeeDevice.get_64bit_addr())
        self.remoteDeviceHumanName = macAddressDictionary[self.macAddress]
        # we dont know if this device is a drone or the base station
        self.classification = None

    def classifyRemoteDevice(self, classification):
        self.classification = classification
