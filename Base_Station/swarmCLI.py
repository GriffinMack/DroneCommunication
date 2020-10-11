import time

import flightControls
import formationControls
from devices import BaseStation


def errorCheckCoordinateValue(coordinate):
    validInput = False
    while not validInput:
        coordinateInput = float(input(f"{coordinate}: "))
        if coordinate == "latitude":
            if -90 <= coordinateInput <= 90:
                validInput = True
        elif coordinate == "longitude":
            if -180 <= coordinateInput <= 180:
                validInput = True
        elif coordinate == "altitude":
            if 0 <= coordinateInput <= 122:  # 122 meters is the max drone hight (FAA)
                validInput = True
    return coordinateInput

def coordinateInputPrompt():
    print("Please input the following coordinates:")
    latitude = errorCheckCoordinateValue("latitude")
    longitude = errorCheckCoordinateValue("longitude")
    altitude = errorCheckCoordinateValue("altitude")
    return (latitude, longitude, altitude)


def moveToCoordinatePrompt(baseStation, droneChoice):
    coordinate = coordinateInputPrompt()
    flightControls.moveToCoordinate(baseStation, coordinate, droneChoice)


def moveFromHomePrompt(baseStation, droneChoice):
    coordinate = coordinateInputPrompt()
    flightControls.moveFromHome(baseStation, coordinate, droneChoice)


def moveFromCurrentPrompt(baseStation, droneChoice):
    coordinate = coordinateInputPrompt()
    flightControls.moveFromCurrent(baseStation, coordinate, droneChoice)


def swarmCreationPrompt(baseStation):
    chosenOption = None
    while chosenOption != "5":
        print(f"    1. form a horizontal line (not tested)")
        print(f"    2. form a horizontal triangle (not tested)")
        print(f"    3. form a vertical line (not implemented)")
        print(f"    4. form a vertical triangle (not implemented)")
        print(f"    5. exit")
        chosenOption = input("Please choose from the options above(input the number):")
        repositionControlOptions = {
            "1": formationControls.formHorizontalLine,
            "2": formationControls.formHorizontalTriangle,
            "3": formationControls.formVerticalLine,
            "4": formationControls.formVerticalTriangle,
        }
        if chosenOption in repositionControlOptions:
            repositionControlOptions[chosenOption](baseStation)
        elif chosenOption == "5":
            print("exiting formation controls")
        else:
            print("invalid option, please try again..")
    flightControls.moveToCoordinate(baseStationXbeeDevice, coordinate, droneChoice)


def repositionDronePrompt(baseStation, droneChoice):
    chosenOption = None
    while chosenOption != "7":
        print(f"    1. move to a certain coordinate")
        print(f"    2. hover at home location")
        print(f"    3. launch the manual control application")
        print(f"    4. follow the base station (not implemented)")
        print(f"    5. move from home location")
        print(f"    6. move from current location")
        print(f"    7. exit")
        chosenOption = input("Please choose from the options above(input the number):")
        repositionControlOptions = {
            "1": moveToCoordinatePrompt,
            "2": flightControls.returnToHomeWithoutLanding,
            "3": flightControls.launchManualControlApplication,
            "4": flightControls.followBaseStationDevice,
            "5": moveFromHomePrompt,
            "6": moveFromCurrentPrompt,
        }
        if chosenOption in repositionControlOptions:
            repositionControlOptions[chosenOption](baseStation, droneChoice)
        elif chosenOption == "5":
            print("exiting reposition controls")
        else:
            print("invalid option, please try again..")


def setMaximumSpeedPrompt(baseStation, droneChoice):
    inputValid = False
    while inputValid is False:
        maxSpeedInput = float(input("Please input a new maximium speed:"))
        # Check that the maximum speed isn't too high (13 m/s should be the max)
        if 0 < maxSpeedInput < 13:
            inputValid = True
    flightControls.setMaximumSpeed(baseStation, maxSpeedInput, droneChoice)


def droneChoicePrompt(baseStation):
    # displays all drones found in the network and prompts the user to decide which drone they want to control. Returns a remoteDrone object
    def errorCheckDroneChoicePrompt():
        validInput = False
        while not validInput:
            try:
                droneChoice = (
                    int(
                        input(
                            "Which drone would you like to control? Input the number:"
                        )
                    )
                    - 1
                )
                # TODO: Remove this check. Only to allow CLI development with no Xbee hardware
                if baseStation.xbee is None:
                    validInput = True
                    droneChoice = 0
                if 0 <= droneChoice < len(droneList):
                    validInput = True
                else:
                    raise Exception
            except:
                print(f"invalid input, enter a number between 1 and {len(droneList)}")
        return droneChoice

    droneList = baseStation.getRemoteDroneList()
    # TODO: Remove this check. Only to allow CLI development with no Xbee hardware
    if baseStation.xbee is not None:
        for num, drone in enumerate(droneList):
            print(f"    {num + 1}. {drone.droneHumanName}")
    else:
        print(f"    1. TEST CLI DRONE")
    return droneList[errorCheckDroneChoicePrompt()]


def droneFlightControlPrompt(baseStation, droneChoice):
    # displays all the current options available for communicating with the drones. Prompts the user for an option until they exit the prompt
    if droneChoice in baseStation.getRemoteDroneList():
        chosenOption = None
        while chosenOption != "8":
            print(f"    1. takeoff")
            print(f"    2. land")
            print(f"    3. reposition drone")
            print(f"    4. grab debug data")
            print(f"    5. grab gps coords")
            print(f"    6. set maximum speed")
            print(f"    7. send any message")
            print(f"    8. exit")
            chosenOption = input(
                "Please choose from the options above(input the number):"
            )

            flightControlChoices = {
                "1": flightControls.takeoff,
                "2": flightControls.landing,
                "3": repositionDronePrompt,
                "4": flightControls.debugData,
                "5": flightControls.gpsData,
                "6": setMaximumSpeedPrompt,
                "7": flightControls.anyMessage,
            }
            if chosenOption in flightControlChoices:
                flightControlChoices[chosenOption](baseStation, droneChoice)
            elif chosenOption == "8":
                print(f"exiting control of {droneChoice.droneHumanName}")
            else:
                print("invalid option, please try again..")
    else:
        print("specified drone not in current network")


def swarmFlightControlPrompt(baseStation):
    # displays all the current options available for communicating with the drones. Prompts the user for an option until they exit the prompt
    chosenOption = None
    while chosenOption != "8":
        print(f"    1. takeoff (not tested)")
        print(f"    2. land (not tested)")
        print(f"    3. reposition drone (not implemented)")
        print(f"    4. grab debug data (not tested)")
        print(f"    5. grab gps coords (not tested)")
        print(f"    6. send any message (not tested)")
        print(f"    7. swarm formation (not tested)")
        print(f"    8. exit")
        chosenOption = input("Please choose from the options above(input the number):")

        flightControlChoices = {
            "1": flightControls.takeoff,
            "2": flightControls.landing,
            # "3": repositionDronePrompt,
            "4": flightControls.debugData,
            "5": flightControls.gpsData,
            "6": flightControls.anyMessage,
            "7": swarmCreationPrompt,
        }
        if chosenOption in flightControlChoices:
            flightControlChoices[chosenOption](baseStation)
        elif chosenOption == "8":
            print("exiting control of multiple drones")
        else:
            print("invalid option, please try again..")


def singleDronePrompt(baseStation):
    # prompts for when the user wants to control just a single drone
    droneChoice = droneChoicePrompt(baseStation)
    droneFlightControlPrompt(baseStation, droneChoice)


def multipleDronePrompt(baseStation):
    # prompts for when the user wants to control multiple drones at once

    if len(baseStation.remoteDroneList) < 2:
        print("Only one drone in the network")
        return
    if "Stanley" not in baseStation.remoteDroneList:
        print("WARNING: Stanley not found. Some swarm functionality may be limited")
    swarmFlightControlPrompt(baseStation)


def systemStartup():
    print("Configuring XBEE..")
    baseStation = BaseStation()
    # print("Adding Message Received Callback..")
    # if baseStation.xbee is not None:
    #     baseStation.addDataReceivedCallback()
    print("System Startup Complete!\n")
    return baseStation


def cliMainMenu():
    baseStation = systemStartup()
    continueUsingCli = True
    while continueUsingCli:
        print("     1. Control a single drone")
        print("     2. Control a drone swarm")
        print("     3. Re-discover the network")
        print("     4. Exit CLI")

        userInput = input("Please choose from the options above(input the number):")

        if userInput == "1":
            singleDronePrompt(baseStation)
        elif userInput == "2":
            multipleDronePrompt(baseStation)
        elif userInput == "3":
            baseStationXbeeDevice.discoverNetwork()
        elif userInput == "4":
            continueUsingCli = False
            baseStation.closeBaseStationXbeeDevice()
        else:
            print("Invalid user input, please try again")


if __name__ == "__main__":
    cliMainMenu()
