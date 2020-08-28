# Griffin Mack
# 8/8/2020
#
# Functions meant to sent specific commands to a drone from the base station
#
#

from Zigbee.sendMessage import sendMessage


def takeoff(device=None):
    print("initiating a takeoff..")
    messageToSend = "takeoff"
    sendMessage(messageToSend, device)


def landing(device=None):
    print("initiating a landing..")
    messageToSend = "land"
    sendMessage(messageToSend, device)


def moveToCoord(device=None, coordinates=None):
    print("moving to inputted coordinates..")
    messageToSend = f"move: {coordinates}"
    sendMessage(messageToSend, device)


def debugData(device=None):
    print("grabbing debug data..")
    messageToSend = "debug"
    sendMessage(messageToSend, device)


def gpsData(device=None):
    print("grabbing GPS data..")
    messageToSend = "gps"
    sendMessage(messageToSend, device)
