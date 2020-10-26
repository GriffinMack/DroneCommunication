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


async def waitForMovementToComplete(
    baseStation, targetCoordinate, droneDevice, leftOrRight
):
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
    print(
        f"{leftOrRight} drone movement complete--- %s seconds ---"
        % (time.time() - start_time)
    )
    return


def getUpdatedDroneLocationTuple(baseStation, droneDevice):
    droneCoordinates = gpsData(baseStation, droneDevice, printMessage=False)
    return (droneDevice, droneCoordinates)


def adjustLat(leftDrone, rightDrone, leftOffset, rightOffset):

    targetCoordinate = (
        leftDrone[1].get("Lat") + leftOffset,
        leftDrone[1].get("Lon"),
        leftDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat") + rightOffset,
        rightDrone[1].get("Lon"),
        rightDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(
                baseStation, targetCoordinate, leftDrone[0], "left"
            )
        ),
        loop.create_task(
            waitForMovementToComplete(
                baseStation, targetCoordinate, rightDrone[0], "right"
            )
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    return leftDrone, rightDrone


def adjustLon(leftDrone, rightDrone, leftOffset, rightOffset):

    targetCoordinate = (
        leftDrone[1].get("Lat"),
        leftDrone[1].get("Lon") + leftOffset,
        leftDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat"),
        rightDrone[1].get("Lon") + rightOffset,
        rightDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(
                baseStation, targetCoordinate, leftDrone[0], "left"
            )
        ),
        loop.create_task(
            waitForMovementToComplete(
                baseStation, targetCoordinate, rightDrone[0], "right"
            )
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    return leftDrone, rightDrone


def adjustAlt(leftDrone, rightDrone, leftOffset, rightOffset):

    targetCoordinate = (
        leftDrone[1].get("Lat"),
        leftDrone[1].get("Lon"),
        leftDrone[1].get("aAlt") + leftOffset,
    )
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat"),
        rightDrone[1].get("Lon"),
        rightDrone[1].get("aAlt") + rightOffset,
    )
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(
                baseStation, targetCoordinate, leftDrone[0], "left"
            )
        ),
        loop.create_task(
            waitForMovementToComplete(
                baseStation, targetCoordinate, rightDrone[0], "right"
            )
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    return leftDrone, rightDrone


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
    # Change the right drone latitude to +0.00003 from the middleDrone
    print("left drone -0.00003 start--- %s seconds ---" % (time.time() - start_time))
    print("right drone +0.00003 start--- %s seconds ---" % (time.time() - start_time))
    leftDrone, rightDrone = adjustLat(
        leftDrone,
        rightDrone,
        (middleDrone[1].get("Lat") - float(0.00003)) - float(leftDrone[1].get("Lat")),
        (middleDrone[1].get("Lat") + float(0.00003)) - float(rightDrone[1].get("Lat")),
    )

    # Get all the drones to the same longitude (middle drone longitude)
    print("left drone long start--- %s seconds ---" % (time.time() - start_time))
    print("right drone long start--- %s seconds ---" % (time.time() - start_time))
    leftDrone, rightDrone = adjustLong(
        leftDrone,
        rightDrone,
        middleDrone[1].get("Lon") - float(leftDrone[1].get("Lon")),
        middleDrone[1].get("Lon") - float(rightDrone[1].get("Lon")),
    )

    # Get all the drones to the same altitude (middle drone altitude)
    print("left drone alt start--- %s seconds ---" % (time.time() - start_time))
    print("right drone alt start--- %s seconds ---" % (time.time() - start_time))
    leftDrone, rightDrone = adjustAlt(
        leftDrone,
        rightDrone,
        middleDrone[1].get("aAlt") - float(leftDrone[1].get("aAlt")),
        middleDrone[1].get("aAlt") - float(rightDrone[1].get("aAlt")),
    )

    currentFormation = {
        "formationType": "3Line",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": 0,
    }
    baseStation.setCurrentFormation(currentFormation)

    return leftDrone, middleDrone, rightDrone


def formHorizontalTriangleThreeDrones(baseStation):
    leftDrone, middleDrone, rightDrone = formHorizontalLineThreeDrones(baseStation)

    # move the leftDrone and rightDrone backwards
    leftDrone, rightDrone = adjustLon(leftDrone, rightDrone, -0.00003, -0.00003)

    currentFormation = {
        "formationType": "3Triangle",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": 0,
    }
    baseStation.setCurrentFormation(currentFormation)

    return leftDrone, middleDrone, rightDrone


def rotateSwarm(baseStation):
    # Use case for 3 drones, probably just move 1 drone for 2 drone case
    # formation is a dict to hold the current formation type, droneTuple and current rotation

    # formation = {
    #       formationType: "3Line",
    #       droneTuple: (leftDrone, middleDrone, rightDrone),
    #       rotation: 90
    # }
    currentFormation = baseStation.getCurrentFormation()

    formationType = currentFormation.get("formationType")
    droneTuple = currentFormation.get("droneTuple")
    rotation = currentFormation.get("rotation")

    formationOptions = {
        "3Line": horizontalLineRotate,
        "3Triangle": horizontalTriangleRotate,
    }

    if formationType in formationOptions:
        # Returns new formation object
        formation = formationOptions[formationType](baseStation, droneTuple, rotation)
    else:
        print(f"Formation {formationType} is unknown")

    baseStation.setCurrentFormation(formation)


def horizontalLineRotate(baseStation, droneTuple, rotation):

    leftDrone, middleDrone, rightDrone = droneTuple

    rotationControl = {
        0: (1, 1, 1),
        90: (0, 1, -1),
        180: (1, -1, -1),
        270: (0, -1, 1),
    }

    if rotation in rotationControl:
        order, latMult, lonMult = rotationControl[rotation]
    else:
        print("Only support 90 degree rotations")

    if order is 1:
        leftDrone, rightDrone = adjustLon(
            leftDrone, rightDrone, lonMult * 0.00003, -lonMult * 0.00003
        )
        adjustLat(leftDrone, rightDrone, latMult * 0.00003, -latMult * 0.00003)
    else:
        leftDrone, rightDrone = adjustLat(
            leftDrone, rightDrone, latMult * 0.00003, -latMult * 0.00003
        )
        adjustLon(leftDrone, rightDrone, lonMult * 0.00003, -lonMult * 0.00003)

    newFormation = {
        "formationType": "3Line",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": (rotation + 90) % 360,
    }

    return newFormation


def horizontalTriangleRotate(baseStation, droneTuple, rotation):

    leftDrone, middleDrone, rightDrone = droneTuple

    rotationControl = {
        0: (1, 1, 1),
        90: (0, 1, -1),
        180: (1, -1, -1),
        270: (0, -1, 1),
    }

    if rotation in rotationControl:
        order, latMult, lonMult = rotationControl[rotation]
    else:
        print("Only support 90 degree rotations")

    if order is 1:
        leftDrone, rightDrone = adjustLon(leftDrone, rightDrone, lonMult * 0.00006, 0)
        adjustLat(leftDrone, rightDrone, 0, latMult * 0.00006)
    else:
        leftDrone, rightDrone = adjustLat(leftDrone, rightDrone, latMult * 0.00006, 0)
        adjustLon(leftDrone, rightDrone, 0, lonMult * 0.00006)

    newFormation = {
        "formationType": "3Triangle",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": (rotation + 90) % 360,
    }

    return newFormation