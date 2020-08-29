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
            device = DigiMeshDevice(port, 9600)
            device.open()
            correctPort = port
        except Exception:
            pass
    return correctPort


def openBaseStationXBEE():
    correctSerialPort = findCorrectSerialPort()
    device = DigiMeshDevice(correctSerialPort, 9600)
    connected = False
    while not connected:
        try:
            device.open()
            connected = True
        except Exception:
            # TODO: Weird issue with double exception. Doesn't bother anything but the printout is really annoying
            pass

    return device
