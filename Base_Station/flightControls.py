# Griffin Mack
# 8/8/2020
#
# Functions meant to sent specific commands to a drone from the base station
#
#

from flightControlApplication.arrowKey import controlDronesManually
import json


def takeoff(baseStation, droneDevice=None):
    print("initiating a takeoff..")
    messageToSend = "takeoff"
    baseStation.sendMessage(messageToSend, droneDevice)


def landing(baseStation, droneDevice=None):
    print("initiating a landing..")
    messageToSend = "land"
    baseStation.sendMessage(messageToSend, droneDevice)


def moveToCoordinate(baseStation, coordinate, droneDevice=None):
    messageToSend = f"move to coordinate:{coordinate}"
    baseStation.sendMessage(messageToSend, droneDevice)


def moveFromHome(baseStation, coordinate, droneDevice=None):
    messageToSend = f"move from home:{coordinate}"
    baseStation.sendMessage(messageToSend, droneDevice)


def moveFromCurrent(baseStation, coordinate, droneDevice=None):
    messageToSend = f"move from current:{coordinate}"
    baseStation.sendMessage(messageToSend, droneDevice)


def returnToHomeWithoutLanding(baseStation, droneDevice=None):
    messageToSend = "return to home without landing"
    baseStation.sendMessage(messageToSend, droneDevice)


def followBaseStationDevice(baseStation, droneDevice=None):
    messageToSend = "follow me"
    baseStation.sendMessage(messageToSend, droneDevice)


def launchManualControlApplication(baseStation, droneDevice=None):
    messageToSend = "manual control"
    baseStation.sendMessage(messageToSend, droneDevice)
    controlDronesManually(baseStation)


def debugData(baseStation, droneDevice=None):
    print("grabbing debug data..")
    messageToSend = "debug"
    baseStation.sendMessage(messageToSend, droneDevice)
    # TODO: This can get interupted by a GPS coordinate broadcast.
    # wait for a message to come back (message is automatically printed)
    receivedMessage = baseStation.pollForIncomingMessage()

    # the message will be a JSON string. turn it into a python dictionary
    return json.loads(receivedMessage)


def gpsData(baseStation, droneDevice=None):
    print("grabbing GPS data..")
    messageToSend = "gps"
    baseStation.sendMessage(messageToSend, droneDevice)

    # wait for a message to come back (message is automatically printed)
    receivedMessage = baseStation.pollForIncomingMessage()

    # the message will be a JSON string. turn it into a python dictionary
    return json.loads(receivedMessage)


def setMaximumSpeed(baseStation, maximumSpeed, droneDevice=None):
    print(f"setting maximum speed to {maximumSpeed} m/s")
    messageToSend = f"set maximum speed:{maximumSpeed}"
    baseStation.sendMessage(messageToSend, droneDevice)


def anyMessage(baseStation, droneDevice=None):
    messageToSend = input("Type the message you would like to send:")
    baseStation.sendMessage(messageToSend, droneDevice)
