# Griffin Mack
# 8/29/2020

#
# Main loop to be ran on the Raspberry Pi. Should be started on power up
#
import time
import asyncio

from Devices.Drone import Drone
from flightControls import (
    calibrateDevice,
    getDroneCoordinates,
    decodeMessage,
)
from collisionAvoidance import (
    establishGeofence,
    collisionAvoidanceBroadcastCheck,
    updateDroneCoordinate,
)


def promptUserForTestInput():
    message = input("Please enter a command: ")
    return message


def systemStartup():
    # The drone class contains connections to the xbee and the pixhawk
    droneDevice = Drone()
    # Establish a default geofence
    establishGeofence(droneDevice)
    # Calibrate any sensors
    # calibrateDevice(droneDevice)

    # Add a callback to parse messages received at any time
    # droneDevice.addDataReceivedCallback()

    return droneDevice

async def droneResetListener():
    # Listen for a GPIO button to be pressed
    while true:
        yield True

async def reactToIncomingMessage(droneDevice):
    while True:
        print("-- Waiting for a message..")
        message, sender = await droneDevice.pollForIncomingMessage()
        
        if message:
            returnMessage = await decodeMessage(droneDevice, message, sender)
            if returnMessage:
                await droneDevice.sendMessage(returnMessage, sender)
        


def main():
    droneDevice = systemStartup()

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(collisionAvoidanceBroadcastCheck(droneDevice)),
        loop.create_task(updateDroneCoordinate(droneDevice)),
        loop.create_task(reactToIncomingMessage(droneDevice)),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == "__main__":
    main()
