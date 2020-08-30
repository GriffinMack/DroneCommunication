from digi.xbee.devices import DigiMeshDevice
import serial.tools.list_ports


def findOpenSerialPorts():
    portsList = serial.tools.list_ports.comports()
    serialPorts = []
    for port, desc, hwid in sorted(portsList):
        if desc != "n/a":
            serialPorts.append(port)
    return serialPorts

def openBaseStationXBEE():
    serialPorts = findOpenSerialPorts()
    for port in serialPorts:
        try:
            device = DigiMeshDevice(port, 9600)
            device.open()
        except Exception:
            pass

    return device
