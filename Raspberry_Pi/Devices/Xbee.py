from digi.xbee.devices import DigiMeshDevice
from digi.xbee.models.status import NetworkDiscoveryStatus
from Devices.Remote import remoteDevice

import asyncio
import time
import serial.tools.list_ports


def findOpenSerialPorts():
    # Grabs all open serial ports
    openPortsList = serial.tools.list_ports.comports()
    serialPorts = []
    # reverse allows multiple xbee's to be opened on a PC
    for port, desc, _ in sorted(openPortsList, reverse=True):
        if desc != "n/a":
            serialPorts.append(port)
    return serialPorts
serialPorts = findOpenSerialPorts()

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
            self.remoteDeviceList = ["9999"]
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
        for port in serialPorts:
            try:
                device = DigiMeshDevice(port, 9600)
                device.open()
                serialPorts.remove(port)

                return device
            except Exception as e:
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

    async def sendMessage(self, message, remoteDevice=None):
        # Check if the message is a dictionary. If it is, we want to convert to json and send line by line
        # TODO: Remove this check. Only to allow CLI development with no Xbee hardware
        if self.xbee is None:
            print(f"sending message: {message}")
        elif remoteDevice:
            await self.__sendDirectMessage(message, remoteDevice)
        else:
            await self.__sendBroadcastMessage(message)

    async def pollForIncomingMessage(self):
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
                await asyncio.sleep(1e-3)
            return xbeeMessage.data.decode()
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
    async def __sendDirectMessage(self, message, remoteDevice):
        # sends a message directly to the specified droneDevice
        try:
            # print(
            #     "Sending data to %s >> %s..."
            #     % (remoteDevice.remoteXbee.get_64bit_addr(), message)
            # )
            self.xbee.send_data(remoteDevice.remoteXbee, message)

        finally:
            if self.xbee is not None and self.xbee.is_open():
                # self.xbee.close()
                pass

    async def __sendBroadcastMessage(self, message):
        # sends a message to all drones in the network
        try:

            # print("Sending data to all devices >> %s..." % (message))
            self.xbee.send_data_broadcast(message)

        finally:
            if self.xbee is not None and self.xbee.is_open():
                # self.xbee.close()
                pass

    def __repopulateRemoteDeviceList(self):
        # Clears the drone list and repopulates it based on the current xbeeNetwork
        self.remoteDeviceList.clear()
        for remoteDevice in self.xbeeNetwork.get_devices():
            newRemoteDrone = remoteDevice(remoteDevice)
            self.remoteDeviceList.append(newRemoteDrone)

def findOpenSerialPorts():
    # Grabs all open serial ports
    openPortsList = serial.tools.list_ports.comports()
    serialPorts = []
    # reverse allows multiple xbee's to be opened on a PC
    for port, desc, _ in sorted(openPortsList, reverse=True):
        if desc != "n/a":
            serialPorts.append(port)
    return serialPorts