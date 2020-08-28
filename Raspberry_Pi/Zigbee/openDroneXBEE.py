from digi.xbee.devices import DigiMeshDevice

def openDroneXBEE():
    device = DigiMeshDevice("/dev/tty.usbserial-3", 9600)

    device.open()
    return device
