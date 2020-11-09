from digi.xbee.devices import DigiMeshDevice
from digi.xbee.models.status import NetworkDiscoveryStatus
from mavsdk import System

import asyncio
import time
import serial.tools.list_ports

"""
droneDictionary : dictionary
    HARD CODED!! Contains the names of all the drones we have available relative to their mac address
    TODO: Make this dictionary available to all areas of the project in one location
"""
macAddressDictionary = {
    "0013A20041C6B692": "Bravo",
    "0013A20041C6B69C": "Charlie",
    "0013A2004195CF95": "Base Station",
    "0013A2004192DBC0": "Stanley",
    "9999": "No Zigbee Attached",
}

"""
A class used to represent a pixhawk.
...

Attributes
----------
Methods
-------
"""


class PixhawkDevice:
    def __init__(self):
        self.pixhawkVehicle = self.connectToVehicle()

    def connectToVehicle(self):
        async def simulator(self):
            async def openSimulation():
                return System()

            async def openDrone():
                return System()

            async def connectToSimulator(drone):
                # Serial: serial:///path/to/serial/dev[:baudrate]
                await drone.connect(system_address="serial:///dev/ttyUSB0")
                print("Waiting for drone to connect...")
                async for state in drone.core.connection_state():
                    if state.is_connected:
                        print(f"Drone discovered with UUID: {state.uuid}")
                        self.pixhawkVehicle = drone
                        break

            async def connectToDrone(drone):
                # TODO: Connect to the correct USB device connected to the Pixhawk
                await drone.connect(system_address="serial:///dev/ttyUSB0:921600")
                print("Waiting for drone to connect...")
                async for state in drone.core.connection_state():
                    if state.is_connected:
                        print(f"Drone discovered with UUID: {state.uuid}")
                        self.pixhawkVehicle = drone
                        break

            drone = await openDrone()
            await connectToDrone(drone)

        # Start SITL if no pixhawk device is found
        loop = asyncio.get_event_loop()
        loop.run_until_complete(simulator(self))
        return self.pixhawkVehicle

    def getPixhawkVehicle(self):
        return self.pixhawkVehicle


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
xbee : <class 'digi.xbee.devices.DigiMeshDevice'>
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
    gets and returns the network that is attached to the xbee device ("getting the network" involves discovering all remote devices that have the same NodeID as the xbee device).
sendMessage(message, remoteDevice=None)
    sends out the inputted message. Depending on if a remoteDevice is specified, the message will either be direct or a broadcast
pollForIncomingMessage()
    blocking function that waits for a message. Returns the data contained in the message once received
addDataReceivedCallback()
    add the option for the base station to accept messages it didn't request. Add to this function if you want functionality based on the incoming message
closeXbeeDevice()
    closes the serial connection to the base station xbee
"""


class XbeeDevice:
    def __init__(self):
        self.xbee = self.openDroneXbee()
        self.remoteDeviceList = []  # the discover network script will fill this in
        # TODO: Remove this check. Only to allow CLI development with no Xbee hardware
        try:
            self.macAddress = str(self.xbee.get_64bit_addr())
        except AttributeError:
            self.macAddress = "9999"
            self.remoteDeviceList = [remoteDevice(self.xbee)]
        # we dont need the network until we want to send a direct message
        self.xbeeNetwork = None

    def getXbee(self):
        return self.xbee

    def getRemoteDeviceList(self):
        return self.remoteDeviceList

    def getMacAddress(self):
        return self.macAddress

    def getXbeeNetwork(self):
        return self.xbeeNetwork

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
            self.xbee.open()
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
                    print(
                        "There was an error discovering devices: %s"
                        % status.description
                    )

            self.xbeeNetwork = self.xbee.get_network()
            self.xbeeNetwork.set_discovery_timeout(5)  # 5 seconds.
            self.xbeeNetwork.clear()

            self.xbeeNetwork.add_device_discovered_callback(callback_device_discovered)
            self.xbeeNetwork.add_discovery_process_finished_callback(
                callback_discovery_finished
            )

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
        if self.xbee is None:
            print(f"sending message: {message}")
        elif remoteDevice:
            self.__sendDirectMessage(message, remoteDevice)
        else:
            self.__sendBroadcastMessage(message)

    def pollForIncomingMessage(self):
        try:
            messageReceived = False
            while not messageReceived:
                xbeeMessage = self.xbee.read_data()
                if xbeeMessage is not None:
                    messageReceived = True
                    print(
                        "From %s >> %s"
                        % (
                            xbeeMessage.remote_device.get_64bit_addr(),
                            xbeeMessage.data.decode(),
                        )
                    )
            return xbeeMessage.data.decode(), xbeeMessage.remote_device

        except Exception as e:
            print(e)

    def checkForIncomingMessage(self):
        try:
            xbeeMessage = self.xbee.read_data()
            if xbeeMessage is not None:
                print(
                    "From %s >> %s"
                    % (
                        xbeeMessage.remote_device.get_64bit_addr(),
                        xbeeMessage.data.decode(),
                    )
                )
            return xbeeMessage.data.decode()
        except Exception as e:
            pass

    def closeXbeeDevice(self):
        if self.xbee is not None and self.xbee.is_open():
            self.xbee.close()

    #
    # Private Functions
    # -----------------
    #
    def __sendDirectMessage(self, message, remoteDevice):
        # sends a message directly to the specified droneDevice
        try:
            print(
                "Sending data to %s >> %s..."
                % (macAddressDictionary[str(remoteDevice.get_64bit_addr())], message)
            )
            self.xbee.send_data(remoteDevice, message)
            print("Success")

        finally:
            if self.xbee is not None and self.xbee.is_open():
                # self.xbee.close()
                pass

    def __sendBroadcastMessage(self, message):
        # sends a message to all drones in the network
        try:

            print("Sending data to all devices >> %s..." % (message))
            self.xbee.send_data_broadcast(message)
            print("Success")

        finally:
            if self.xbee is not None and self.xbee.is_open():
                # self.xbee.close()
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
    def __init__(self, remoteXbeeDevice):
        self.remoteXbee = remoteXbeeDevice
        self.macAddress = str(self.remoteXbee.get_64bit_addr())
        self.remoteDeviceHumanName = macAddressDictionary[self.macAddress]
        # we dont know if this device is a drone or the base station
        self.classification = None

    def classifyRemoteDevice(self, classification):
        self.classification = classification


"""
A class used to represent a drone, which is attached to an XBEE device, Pixhawk device, and a ZUBAX device.
...

Attributes
----------
Methods
-------
"""


class Drone(PixhawkDevice, XbeeDevice):
    def __init__(self):
        XbeeDevice.__init__(self)
        PixhawkDevice.__init__(self)
        self.droneHumanName = macAddressDictionary[self.macAddress]
        self.safeDistance = 5  # meters
        self.safeAltitude = 2  # meters

    def getDroneHumanName(self):
        return self.droneHumanName

    def getSafeDistance(self):
        return self.safeDistance

    def getSafeAltitude(self):
        return self.safeAltitude

    def addDataReceivedCallback(self):
        def data_receive_callback(xbee_message):
            print(
                "\nFrom %s >> %s"
                % (
                    xbee_message.remote_device.get_64bit_addr(),
                    xbee_message.data.decode(),
                )
            )

        self.xbee.add_data_received_callback(data_receive_callback)
