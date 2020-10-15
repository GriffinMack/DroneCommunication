# Griffin Mack
# 8/29/2020

#
# Main loop to be ran on the Raspberry Pi. Should be started on power up
#
import time
import asyncio

from devices import Drone
from flightControls import (
    establishGeofence,
    calibrateDevice,
    getDroneCoordinates,
    decodeMessage,
    collisionAvoidanceBroadcastCheck,
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

async def reactToIncomingMessage(droneDevice):
    print("-- Waiting for a message..")
    message = await droneDevice.pollForIncomingMessage()
    if message:
        returnMessage = await decodeMessage(droneDevice, message)
        if returnMessage:
            droneDevice.sendMessage(returnMessage)
    # droneDevice.sendMessage(getDroneCoordinates(droneDevice))

def main():
    droneDevice = systemStartup()
    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            collisionAvoidanceBroadcastCheck(droneDevice)
        ),
        # loop.create_task(
        #     reactToIncomingMessage(droneDevice)
        # ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == "__main__":
    main()
