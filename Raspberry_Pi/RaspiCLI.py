from Zigbee.openDroneXBEE import openDroneXBEE
from Zigbee.receive import receive
from Zigbee.transmit import transmit

def main():
    device = openDroneXBEE()

    while True:
        xbee_message = receive(device)
        device = openDroneXBEE()
        transmit(device, xbee_message)



if __name__ == "__main__":
    main()
