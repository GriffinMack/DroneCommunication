from Zigbee.openDroneXBEE import openDroneXBEE
from Zigbee.receive import receive
from Zigbee.transmit import transmit

def main():
    device = openDroneXBEE()

    while True:
        receive(device)
        device = openDroneXBEE()
        xbeeMessage = "success"
        transmit(device, xbeeMessage)



if __name__ == "__main__":
    main()
