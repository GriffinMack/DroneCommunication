# Griffin Mack
# 8/8/2020
#
# Functions meant to sent specific commands to a drone from the base station
#
#

from flightControlApplication.arrowKey import controlDronesManually
import json


def breakFormationCheck(baseStation, droneDevice):
    # Checks if a formation is already made and the user tries to control a single drone
    if droneDevice and baseStation.getCurrentFormation():
        baseStation.setCurrentFormation(None)


def takeoff(baseStation, droneDevice=None):
    if droneDevice:
        print(f"{droneDevice.getDroneName()} initiating a takeoff..")
    else:
        print("swarm initiating a takeoff..")

    breakFormationCheck(baseStation, droneDevice)
    messageToSend = "takeoff"
    baseStation.sendMessage(messageToSend, droneDevice)


def landing(baseStation, droneDevice=None):
    if droneDevice:
        print(f"{droneDevice.getDroneName()} initiating a landing..")
    else:
        print("swarm initiating a landing..")

    breakFormationCheck(baseStation, droneDevice)
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


def launchManualControlApplication(baseStation, droneDevice=None):
    if droneDevice:
        print(f"{droneDevice.getDroneName()} initiating manual control..")
    else:
        print("swarm initiating manual control..")

    messageToSend = "manual control"
    baseStation.sendMessage(messageToSend, droneDevice)
    controlDronesManually(baseStation, droneDevice)


def debugData(baseStation, droneDevice=None, swarmSize=3, printMessage=True):
    messageToSend = "debug"

    if droneDevice:
        print(f"grabbing {droneDevice.getDroneName()} debug data..")
        baseStation.sendMessage(messageToSend, droneDevice)
        receivedMessage = baseStation.pollForIncomingMessage(Print=printMessage)
    else:
        print("grabbing swarm debug data..")
        baseStation.sendMessage(messageToSend, droneDevice)
        # TODO: right now there is no reason to get the messages, we just want to print it
        baseStation.pollForIncomingMessage(Print=printMessage, amountOfMessages=3)
    # the message will be a JSON string. turn it into a python dictionary
    if receivedMessage:
        return json.loads(receivedMessage)


def gpsData(baseStation, droneDevice=None, printMessage=True):
    messageToSend = "gps"

    if droneDevice:
        print(f"grabbing {droneDevice.getDroneName()} gps data..")
        baseStation.sendMessage(messageToSend, droneDevice)
        receivedMessage = baseStation.pollForIncomingMessage(Print=printMessage)
    else:
        print("grabbing swarm gps data..")
        baseStation.sendMessage(messageToSend, droneDevice)
        # TODO: right now there is no reason to get the messages, we just want to print it
        baseStation.pollForIncomingMessage(Print=printMessage, amountOfMessages=3)
    # the message will be a JSON string. turn it into a python dictionary
    if receivedMessage:
        return json.loads(receivedMessage)


def setMaximumSpeed(baseStation, maximumSpeed, droneDevice=None):
    if droneDevice:
        print(
            f"setting {droneDevice.getDroneName()} maximum speed to {maximumSpeed} m/s.."
        )
    else:
        print(f"setting swarm maximum speed to {maximumSpeed} m/s..")

    messageToSend = f"set maximum speed:{maximumSpeed}"
    baseStation.sendMessage(messageToSend, droneDevice)


def anyMessage(baseStation, droneDevice=None):
    messageToSend = input("Type the message you would like to send:")
    baseStation.sendMessage(messageToSend, droneDevice)
