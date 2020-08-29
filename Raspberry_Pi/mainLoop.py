from Zigbee.openDroneXBEE import openDroneXBEE
from Zigbee.receive import receive
from Zigbee.transmit import transmit


def systemStartup():
    droneDevice = openDroneXBEE()
    return droneDevice


def main():
    droneDevice = systemStartup()

    while True:
        # Wait for a communication from the XBEE
        receive(droneDevice)
        xbeeMessage = "success"
        transmit(droneDevice, xbeeMessage)


if __name__ == "__main__":
    main()
