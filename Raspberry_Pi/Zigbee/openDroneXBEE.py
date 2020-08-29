from digi.xbee.devices import DigiMeshDevice
import serial.tools.list_ports


def findCorrectSerialPort():
    portsList = serial.tools.list_ports.comports()
    serialPorts = []
    for port, desc, hwid in sorted(portsList):
        if desc != "n/a":
            serialPorts.append(port)

    for port in serialPorts:
        try:
            possibleDevice = DigiMeshDevice(port, 9600)
            possibleDevice.open()
            droneXbeeDevice = port
        except Exception:
            pass
    return droneXbeeDevice


def openDroneXBEE():
    correctSerialPort = findCorrectSerialPort()
    droneXbeeDevice = DigiMeshDevice(correctSerialPort, 9600)
    connected = False
    while not connected:
        try:
            droneXbeeDevice.open()
            connected = True
        except Exception:
            # TODO: Weird issue with double exception. Doesn't bother anything but the printout is really annoying
            pass
    return droneXbeeDevice
