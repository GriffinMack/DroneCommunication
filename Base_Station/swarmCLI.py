import time

# local file imports
import flightControls
from Zigbee.applyXbeeProfile import applyProfile
from Zigbee.networkDiscovery import discoverNetwork
def singleDroneChosen(droneList):
    for drone in droneList: print(drone) 
    droneChoice = input("Which drone would you like to control? Input the drone name:")
    if droneChoice in droneList:
        singleDroneOption = "1"
        while singleDroneOption != "6":
            print(f"    1. takeoff")
            print(f"    2. land")
            print(f"    3. move to Coordinates")
            print(f"    4. grab debug data")
            print(f"    5. grab gps coords")
            print(f"    6. exit")
            singleDroneOption = input("Please choose from the options above(input the number):")

            if singleDroneOption == "1":
                # initiate a takeoff from the current position
                flightControls.takeoff()
            elif singleDroneOption == "2":
                # initiate landing (possibly add different landing options)
                flightControls.landing()
            elif singleDroneOption == "3":
                # move to inputted coordinates
                flightControls.moveToCoord()
            elif singleDroneOption == "4":
                # grab debug data and display it to the user
                flightControls.debugData()
            elif singleDroneOption == "5":
                # grab GPS coordinate and display it to the user
                flightControls.gpsData()
            elif singleDroneOption == "6":
                # exit the prompt
                print(f"exiting control of drone {droneChoice}")
            else:
                print(f"invalid option, please try again..")
            time.sleep(5)
    else:
        print("specified drone not in current network")

def systemStartup():
    print("Starting up swarm sequence...")

    print("Configuring XBEE.."),
    # call script to configure on board XBEE
    applyProfile()

    print("Finding drones in the network..\n")
    # call script to discover other XBEE's in the network

def main():
    systemStartup()
    droneList = discoverNetwork()
    while True:
        print("     1. Control a single drone")
        print("     2. Control a drone swarm")
        userInput = input("Please choose from the options above(input the number):")

        if userInput == "1":
            singleDroneChosen(droneList)
        elif userInput == "2":
            print("User has chosen drone swarm")
        else:
            print("Invalid user input, please try again")



if __name__ == "__main__":
    main()
