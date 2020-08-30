# Griffin Mack
# 8/8/2020
#
# Functions meant to sent specific commands to a drone from the base station
#
#

from Zigbee.sendMessage import sendMessage


def takeoff(device, baseStationXbeeDevice):
    print("initiating a takeoff..")
    messageToSend = "takeoff"
    sendMessage(messageToSend, device, baseStationXbeeDevice)


def landing(device, baseStationXbeeDevice):
    print("initiating a landing..")
    messageToSend = "land"
    sendMessage(messageToSend, device,  baseStationXbeeDevice)


def moveToCoord(device, coordinates, baseStationXbeeDevice):
    print("moving to inputted coordinates..")
    messageToSend = f"move: {coordinates}"
    sendMessage(messageToSend, device, baseStationXbeeDevice)


def debugData(device, baseStationXbeeDevice):
    print("grabbing debug data..")
    messageToSend = "debug"
    sendMessage(messageToSend, device, baseStationXbeeDevice)


def gpsData(device, baseStationXbeeDevice):
    print("grabbing GPS data..")
    messageToSend = "gps"
    sendMessage(messageToSend, device, baseStationXbeeDevice)
