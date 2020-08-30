import time

# local file imports
import flightControls
from Zigbee.applyXbeeProfile import applyProfile
from Zigbee.networkDiscovery import discoverNetwork
from Zigbee.openBaseStationXBEE import openBaseStationXBEE

droneDictionary = {
    "0013A20041C6B692": "Griffin's test drone",
    "0013A20041C6B69C": "Griffin's base station",
    "0000": "Stanley",
    "0001": "Charlie",
    "0002": "Bravo"
}


deviceDictionary = {
}


def renameDiscoveredDevices(xbee_network):
    devicesList = xbee_network.get_devices()
    droneList = []
    for device in devicesList:
        deviceAddressString = str(device.get_64bit_addr())
        if deviceAddressString in droneDictionary:
            droneName = droneDictionary[deviceAddressString]
            droneList.append(droneName)
            deviceDictionary[droneName] = device
    return droneList


def findDeviceFromDroneName(droneName):
    return deviceDictionary[droneName]


def singleDroneChosen(xbee_network, baseStationXbeeDevice):
    droneList = renameDiscoveredDevices(xbee_network)
    for drone in droneList:
        print(drone)
    droneChoice = input(
        "Which drone would you like to control? Input the drone name:")
    if droneChoice in droneList:
        deviceChoice = findDeviceFromDroneName(droneChoice)
        singleDroneOption = "1"
        while singleDroneOption != "6":
            print(f"    1. takeoff")
            print(f"    2. land")
            print(f"    3. move to Coordinates")
            print(f"    4. grab debug data")
            print(f"    5. grab gps coords")
            print(f"    6. exit")
            singleDroneOption = input(
                "Please choose from the options above(input the number):")

            if singleDroneOption == "1":
                # initiate a takeoff from the current position
                flightControls.takeoff(deviceChoice, baseStationXbeeDevice)
            elif singleDroneOption == "2":
                # initiate landing (possibly add different landing options)
                flightControls.landing(deviceChoice, baseStationXbeeDevice)
            elif singleDroneOption == "3":
                # TODO: prompt user for coordinates
                coordinates = (0, 0, 0)
                flightControls.moveToCoord(
                    deviceChoice, coordinates, baseStationXbeeDevice)
            elif singleDroneOption == "4":
                # grab debug data and display it to the user
                flightControls.debugData(deviceChoice, baseStationXbeeDevice)
            elif singleDroneOption == "5":
                # grab GPS coordinate and display it to the user
                flightControls.gpsData(deviceChoice, baseStationXbeeDevice)
            elif singleDroneOption == "6":
                # exit the prompt
                print(f"exiting control of drone {droneChoice}")
            else:
                print(f"invalid option, please try again..")
    else:
        print("specified drone not in current network")


def systemStartup():
    def data_receive_callback(xbee_message):
        print("\nFrom %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                 xbee_message.data.decode()))
    print("Configuring XBEE..")
    baseStationXbeeDevice = openBaseStationXBEE()
    print("Finding drones in the network..")
    xbeeNetwork = discoverNetwork(baseStationXbeeDevice)
    print("Adding message listener..")

    baseStationXbeeDevice.add_data_received_callback(data_receive_callback)
    print("System Startup Complete!\n")
    return baseStationXbeeDevice, xbeeNetwork


def main():
    baseStationXbeeDevice, xbeeNetwork = systemStartup()

    while True:
        print("     1. Control a single drone")
        print("     2. Control a drone swarm")
        userInput = input(
            "Please choose from the options above(input the number):")

        if userInput == "1":
            singleDroneChosen(xbeeNetwork, baseStationXbeeDevice)
        elif userInput == "2":
            print("User has chosen drone swarm")
        else:
            print("Invalid user input, please try again")


if __name__ == "__main__":
    main()
