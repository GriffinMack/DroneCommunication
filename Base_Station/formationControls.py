# Griffin Mack
# 9/21/2020
#
# Functions meant to form a formation with multiple drones
#
#
from devices import BaseStation
from flightControls import gpsData, moveFromCurrent, moveToCoordinate
from math import isclose
import time
import asyncio

async def waitForMovementToComplete(baseStation, targetCoordinate, droneDevice, leftOrRight):
    targetLat = targetCoordinate[0]
    targetLon = targetCoordinate[1]
    targetAlt = targetCoordinate[2]

    currentGPSLocation = gpsData(baseStation, droneDevice, printMessage=False)
    currentLat = currentGPSLocation["Lat"]
    currentLon = currentGPSLocation["Lon"]
    currentAlt = currentGPSLocation["aAlt"]

    # Check if the coordinate is close to the target (will vary by about 0.5m max)
    while (
        isclose(currentLat, targetLat, abs_tol=5e-6) is False
        or isclose(currentLon, targetLon, abs_tol=5e-6) is False
        or isclose(currentAlt, targetAlt, abs_tol=5e-1) is False
    ):
        await asyncio.sleep(0.5)
        currentGPSLocation = gpsData(baseStation, droneDevice, printMessage=False)
        currentLat = currentGPSLocation["Lat"]
        currentLon = currentGPSLocation["Lon"]
        currentAlt = currentGPSLocation["aAlt"]
    print(f"{leftOrRight} drone movement complete--- %s seconds ---" % (time.time() - start_time))
    return


def getUpdatedDroneLocationTuple(baseStation, droneDevice):
    droneCoordinates = gpsData(baseStation, droneDevice, printMessage=False)
    return (droneDevice, droneCoordinates)


def formHorizontalLineThreeDrones(baseStation):
    print("Forming a horizontal line with three drones..")

    # gather all the discovered drone coordinates
    droneList = baseStation.getRemoteDroneList()
    coordinateList = []
    for droneDevice in droneList:
        droneCoordinates = gpsData(baseStation, droneDevice, printMessage=False)
        coordinateList.append((droneDevice, droneCoordinates))

    # Find the drone with the largest Latitude() and make it the left drone
    # 'lambda item:item[1]["Lat"]' returns the latitude for each item in the coordinate list
    leftDrone = max(coordinateList, key=lambda item: item[1].get("Lat"))
    # Find the drone with the smallest Latitude() and make it the right drone
    rightDrone = min(coordinateList, key=lambda item: item[1].get("Lat"))

    # Leftover drone is the middle drone
    for droneTuple in coordinateList:
        if droneTuple is not leftDrone or rightDrone:
            middleDrone = droneTuple

    global start_time
    start_time = time.time()

    # Change the left drone latitude to -0.00003 from the middleDrone
    targetCoordinate = (
        float(middleDrone[1].get("Lat")) - float(0.00003),
        leftDrone[1].get("Lon"),
        leftDrone[1].get("aAlt"),
    )
    print("left drone -0.00003 start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    # Change the right drone latitude to +0.00003 from the middleDrone
    targetCoordinate = (
        float(middleDrone[1].get("Lat")) + float(0.00003),
        rightDrone[1].get("Lon"),
        rightDrone[1].get("aAlt"),
    )
    print("right drone +0.00003 start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0], 'left')
        ),
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0], 'right')
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    # Get all the drones to the same longitude
    targetCoordinate = (
        leftDrone[1].get("Lat"),
        middleDrone[1].get("Lon"),
        leftDrone[1].get("aAlt"),
    )
    print("left drone long start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat"),
        middleDrone[1].get("Lon"),
        rightDrone[1].get("aAlt"),
    )
    print("right drone long start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0], 'left')
        ),
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0], 'right')
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    # Get all the drones to the same altitude
    targetCoordinate = (
        leftDrone[1].get("Lat"),
        leftDrone[1].get("Lon"),
        middleDrone[1].get("aAlt"),
    )
    print("left drone alt start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat"),
        rightDrone[1].get("Lon"),
        middleDrone[1].get("aAlt"),
    )
    print("right drone alt start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0], 'left')
        ),
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0], 'right')
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    return leftDrone, middleDrone, rightDrone


def formHorizontalTriangleThreeDrones(baseStation):
    leftDrone, middleDrone, rightDrone = formHorizontalLineThreeDrones(baseStation)
    # move the leftDrone and rightDrone backwards
    targetCoordinate = (0, -0.00003, 0)

    moveFromCurrent(baseStation, targetCoordinate, leftDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0], 'left')

    targetCoordinate = (0, -0.00003, 0)

    moveFromCurrent(baseStation, targetCoordinate, rightDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0], 'right')

def formHorizontalLineTwoDrones(baseStation):
    print("Forming a horizontal line with three drones..")

    # gather all the discovered drone coordinates
    droneList = baseStation.getRemoteDroneList()
    coordinateList = []
    for droneDevice in droneList:
        droneCoordinates = gpsData(baseStation, droneDevice, printMessage=False)
        coordinateList.append((droneDevice, droneCoordinates))

    # Find the drone with the largest Latitude() and make it the left drone
    # 'lambda item:item[1]["Lat"]' returns the latitude for each item in the coordinate list
    leftDrone = max(coordinateList, key=lambda item: item[1].get("Lat"))
    # Find the drone with the smallest Latitude() and make it the right drone
    rightDrone = min(coordinateList, key=lambda item: item[1].get("Lat"))

    centerLat = (leftDrone[1].get("Lat") + rightDrone[1].get("Lat"))/2

    global start_time
    start_time = time.time()

    # Change the left drone latitude to -0.00003 from the middleDrone
    targetCoordinate = (
        float(centerLat - float(0.000015)),
        leftDrone[1].get("Lon"),
        leftDrone[1].get("aAlt"),
    )
    print("left drone -0.000015 start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    # Change the right drone latitude to +0.00003 from the middleDrone
    targetCoordinate = (
        float(centerLat + float(0.000015)),
        rightDrone[1].get("Lon"),
        rightDrone[1].get("aAlt"),
    )
    print("right drone +0.000015 start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0], 'left')
        ),
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0], 'right')
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    centerLon = (leftDrone[1].get("Lon") + rightDrone[1].get("Lon"))/2

 # Get all the drones to the same longitude
    targetCoordinate = (
        leftDrone[1].get("Lat"),
        centerLon,
        leftDrone[1].get("aAlt"),
    )
    print("left drone long start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat"),
        centerLon,
        rightDrone[1].get("aAlt"),
    )
    print("right drone long start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0], 'left')
        ),
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0], 'right')
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    centerAlt = (leftDrone[1].get("aAlt") + rightDrone[1].get("aAlt"))/2

# Get all the drones to the same altitude
    targetCoordinate = (
        leftDrone[1].get("Lat"),
        leftDrone[1].get("Lon"),
        centerAlt,
    )
    print("left drone alt start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat"),
        rightDrone[1].get("Lon"),
        centerAlt,
    )
    print("right drone alt start--- %s seconds ---" % (time.time() - start_time))
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0], 'left')
        ),
        loop.create_task(
            waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0], 'right')
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    centerPoint = ("Center", {centerLat, centerLon, centerAlt})

    return leftDrone, centerPoint, rightDrone