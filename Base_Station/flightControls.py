# Griffin Mack
# 8/8/2020
# 
# File contains all the pre-defined functionality 
# 
#
    
from Zigbee.sendMessage import sendMessage
    
    
    
    
    # we want to tell the raspberry pi to send a takeoff command
    # on the base station end:
    #       creating a message to send
    #       sending a message through the base station Zigbee
    #       waiting for an acknolodgement of reception
    # on the Raspberry Pi end:
    #       receiving a message
    #       interpreting the message


def takeoff():

    print("initiating a takeoff..")

def landing():
    print("initiating a landing..")

def moveToCoord():
    print("moving to inputted coordinates..")

def debugData():
    print("grabbing debug data..")

def gpsData():
    print("grabbing GPS data..")