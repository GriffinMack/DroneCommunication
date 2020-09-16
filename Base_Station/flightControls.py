# Griffin Mack
# 8/8/2020
#
# Functions meant to sent specific commands to a drone from the base station
#
#

from flightControlApplication.arrowKey import controlDronesManually


def takeoff(baseStationXbeeDevice, droneDevice=None):
    print("initiating a takeoff..")
    messageToSend = "takeoff"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def landing(baseStationXbeeDevice, droneDevice=None):
    print("initiating a landing..")
    messageToSend = "land"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def moveToCoordinate(baseStationXbeeDevice, coordinate, droneDevice=None):
    messageToSend = f"move to coordinate:{coordinate}"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def returnToHomeWithoutLanding(baseStationXbeeDevice, droneDevice=None):
    messageToSend = "return to home without landing"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def followBaseStationDevice(baseStationXbeeDevice, droneDevice=None):
    messageToSend = "follow me"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def launchManualControlApplication(baseStationXbeeDevice, droneDevice=None):
    messageToSend = "manual control"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)
    controlDronesManually(baseStationXbeeDevice)


def debugData(baseStationXbeeDevice, droneDevice=None):
    print("grabbing debug data..")
    messageToSend = "debug"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)

    # wait for a message to come back (message is automatically printed)
    for message in range(6):   # Poll 6 times for data
        baseStationXbeeDevice.pollForIncomingMessage()


def gpsData(baseStationXbeeDevice, droneDevice=None):
    print("grabbing GPS data..")
    messageToSend = "gps"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)

    # wait for a message to come back (message is automatically printed)
    baseStationXbeeDevice.pollForIncomingMessage()


def anyMessage(baseStationXbeeDevice, droneDevice=None):
    messageToSend = input("Type the message you would like to send:")
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)
