from digi.xbee.devices import DigiMeshDevice

def openBaseStationXBEE():
    device = DigiMeshDevice("/dev/tty.usbserial-0001", 9600)

    device.open()
    return device