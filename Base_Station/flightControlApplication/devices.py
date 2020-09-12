from digi.xbee.devices import DigiMeshDevice
import serial.tools.list_ports
from digi.xbee.models.status import NetworkDiscoveryStatus
import time
import json

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
A class used to represent the base station, which is attached to an XBEE device.
...

Attributes
----------
localXbeeDevice : <class 'digi.xbee.devices.DigiMeshDevice'>
    Contains useful info/methods. See Xbee python library for more info
macAddress : str
    The mac address of the xbee connected to the drone. Can be found under the xbee device hardware
baseStationHumanName : str
    A human readable name for the base station xbee device
remoteDroneList : List[remoteDrone]
    A list of all the remote drones currently found in the network
xbeeNetwork : xbeeNetwork object
    Contains useful info/methods about the discovered xbee network. See Xbee python library for more info
Methods
-------
openBaseStationXbee()
    checks all laptop serial ports and finds the one with an Xbee plugged into it. returns the opened device
discoverNetwork()
    gets and returns the network that is attached to the local xbee device ("getting the network" involves discovering all remote devices that have the same NodeID as the local xbee device).
sendMessage(message, remoteDroneDevice=None)
    sends out the inputted message. Depending on if a remoteDroneDevice is specified, the message will either be direct or a broadcast
pollForIncomingMessage()
    blocking function that waits for a message. Returns the data contained in the message once received
addDataReceivedCallback()
    add the option for the base station to accept messages it didn't request. Add to this function if you want functionality based on the incoming message
closeBaseStationXbeeDevice()
    closes the serial connection to the base station xbee
"""


class baseStation:
    def __init__(self):
        self.localXbeeDevice = self.openBaseStationXbee()
        self.remoteDroneList = []  # the discover network script will fill this in
        # TODO: Remove this check. Only to allow CLI development with no Xbee hardware
        try:
            self.macAddress = str(self.localXbeeDevice.get_64bit_addr())
        except AttributeError:
            self.macAddress = "9999"
            self.remoteDroneList = ["9999"]
        self.baseStationHumanName = macAddressDictionary[self.macAddress]

    def openBaseStationXbee(self):
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
            self.__repopulateRemoteDroneList()  # update the remote drone list
            return self.xbeeNetwork

        except Exception as e:
            print(e)

    def sendMessage(self, message, remoteDroneDevice=None):
        # TODO: Remove this check. Only to allow CLI development with no Xbee hardware
        if self.localXbeeDevice is None:
            print(f"sending message: {message}")
        elif remoteDroneDevice:
            self.__sendDirectMessage(message, remoteDroneDevice)
        else:
            self.__sendBroadcastMessage(message)

    def pollForIncomingMessage(self):
        try:
            messageReceived = False
            while not messageReceived:
                xbeeMessage = self.localXbeeDevice.read_data()
                if xbeeMessage is not None:
                    messageReceived = True
                    self.printReceivedMessage(xbeeMessage)
                    return xbeeMessage.data.decode()
        except Exception as e:
            print(e)

    def addDataReceivedCallback(self):
        def data_receive_callback(xbeeMessage):
            decodedMessage = xbeeMessage.data.decode()
            # supress the print if the data coming back is JSON
            if(decodedMessage[0] != "{"):
                self.__printReceivedMessage(xbeeMessage)
        self.localXbeeDevice.add_data_received_callback(data_receive_callback)

    def closeBaseStationXbeeDevice(self):
        if self.localXbeeDevice is not None and self.localXbeeDevice.is_open():
            self.localXbeeDevice.close()

#
# Private Functions
# -----------------
#
    def __printReceivedMessage(self, xbeeMessage):
        # takes the decoded message and decides how to display it (all messages will be a string)
        decodedMessage = xbeeMessage.data.decode()
        messageSender = xbeeMessage.remote_device.get_64bit_addr()
        if(decodedMessage[0] == "{"):
            jsonObject = json.loads(decodedMessage)
            jsonFormattedString = json.dumps(jsonObject, indent=2)
            print(f"\nfrom {messageSender} >> {jsonFormattedString}\n")
        else:
            print(f"\nfrom {messageSender} >> {decodedMessage}\n")

    def __sendDirectMessage(self, message, droneDevice):
        # sends a message directly to the specified droneDevice
        try:
            print("Sending data to %s >> %s..." %
                  (droneDevice.remoteXbeeDevice.get_64bit_addr(), message))
            self.localXbeeDevice.send_data(
                droneDevice.remoteXbeeDevice, message)

        finally:
            if self.localXbeeDevice is not None and self.localXbeeDevice.is_open():
                # self.localXbeeDevice.close()
                pass

    def __sendBroadcastMessage(self, message):
        # sends a message to all drones in the network
        try:

            print("Sending data to all devices >> %s..." % (message))
            self.localXbeeDevice.send_data_broadcast(message)
        finally:
            if self.localXbeeDevice is not None and self.localXbeeDevice.is_open():
                # self.localXbeeDevice.close()
                pass

    def __findOpenSerialPorts(self):
        # Grabs all open serial ports
        openPortsList = serial.tools.list_ports.comports()
        serialPorts = []
        for port, desc, _ in sorted(openPortsList):
            if desc != "n/a":
                serialPorts.append(port)
        return serialPorts

    def __repopulateRemoteDroneList(self):
        # Clears the drone list and repopulates it based on the current xbeeNetwork
        self.remoteDroneList.clear()
        for remoteDevice in self.xbeeNetwork.get_devices():
            newRemoteDrone = remoteDrone(remoteDevice)
            self.remoteDroneList.append(newRemoteDrone)


"""
A class used to represent a drone that is connected to the base station via a remote connection
...

Attributes
----------
remoteXbeeDevice : digimesh xbee remote device
    Contains useful info/methods. See Xbee python library for more info
macAddress : str
    The mac address of the xbee connected to the drone. Can be found under the xbee device hardware
droneHumanName : str
    Friendlier names for the drones so we don't have to talk about them with their mac addresses

Methods
-------
"""


class remoteDrone:

    def __init__(self, remoteXbeeDevice):
        self.remoteXbeeDevice = remoteXbeeDevice
        self.macAddress = str(remoteXbeeDevice.get_64bit_addr())
        self.droneHumanName = macAddressDictionary[self.macAddress]
