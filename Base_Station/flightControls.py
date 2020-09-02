# Griffin Mack
# 8/8/2020
#
# Functions meant to sent specific commands to a drone from the base station
#
#

from flightControlApplication.arrowKeys import controlDronesManually


def takeoff(baseStationXbeeDevice, droneDevice=None):
    print("initiating a takeoff..")
    messageToSend = "takeoff"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def landing(baseStationXbeeDevice, droneDevice=None):
    print("initiating a landing..")
    messageToSend = "land"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def moveToCoordinate(baseStationXbeeDevice, coordinate, droneDevice=None):
    # option to reposition by sending a coordinate
    messageToSend = f"move to coordinate: {coordinate}"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def returnToHomeWithoutLanding(baseStationXbeeDevice, droneDevice=None):
    # option to return to the home location (hover above)
    messageToSend = "return to home without landing"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def followBaseStationDevice(baseStationXbeeDevice, droneDevice=None):
    # option to follow the base station as it moves around
    messageToSend = "follow me"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def launchManualControlApplication(baseStationXbeeDevice, droneDevice=None):
    # option to launch the key logger and manually fly the drone
    controlDronesManually(baseStationXbeeDevice)


def debugData(baseStationXbeeDevice, droneDevice=None):
    print("grabbing debug data..")
    messageToSend = "debug"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)


def gpsData(baseStationXbeeDevice, droneDevice=None):
    print("grabbing GPS data..")
    messageToSend = "gps"
    baseStationXbeeDevice.sendMessage(messageToSend, droneDevice)
