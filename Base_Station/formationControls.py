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


def adjustLat(baseStation, leftDrone, rightDrone, leftOffset, rightOffset):

    leftTargetCoordinate = (
        round((leftDrone[1].get("Lat") + leftOffset), 6),
        round(leftDrone[1].get("Lon"), 6),
        round(leftDrone[1].get("aAlt"), 6),
    )
    moveToCoordinate(baseStation, leftTargetCoordinate, leftDrone[0])

    rightTargetCoordinate = (
        round((rightDrone[1].get("Lat") + rightOffset), 6),
        round(rightDrone[1].get("Lon"), 6),
        round(rightDrone[1].get("aAlt"), 6),
    )
    moveToCoordinate(baseStation, rightTargetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(
                baseStation, leftTargetCoordinate, leftDrone[0], "left"
            )
        ),
        loop.create_task(
            waitForMovementToComplete(
                baseStation, rightTargetCoordinate, rightDrone[0], "right"
            )
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    return leftDrone, rightDrone


def adjustLon(baseStation, leftDrone, rightDrone, leftOffset, rightOffset):

    leftTargetCoordinate = (
        round(leftDrone[1].get("Lat"), 6),
        round((leftDrone[1].get("Lon") + leftOffset), 6),
        round(leftDrone[1].get("aAlt"), 6),
    )
    moveToCoordinate(baseStation, leftTargetCoordinate, leftDrone[0])

    rightTargetCoordinate = (
        round(rightDrone[1].get("Lat"), 6),
        round((rightDrone[1].get("Lon") + rightOffset), 6),
        round(rightDrone[1].get("aAlt"), 6),
    )
    moveToCoordinate(baseStation, rightTargetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(
                baseStation, leftTargetCoordinate, leftDrone[0], "left"
            )
        ),
        loop.create_task(
            waitForMovementToComplete(
                baseStation, rightTargetCoordinate, rightDrone[0], "right"
            )
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    return leftDrone, rightDrone


def adjustAlt(baseStation, leftDrone, rightDrone, leftOffset, rightOffset):

    leftTargetCoordinate = (
        round(leftDrone[1].get("Lat"), 6),
        round(leftDrone[1].get("Lon"), 6),
        round((leftDrone[1].get("aAlt") + leftOffset), 6),
    )
    moveToCoordinate(baseStation, leftTargetCoordinate, leftDrone[0])

    rightTargetCoordinate = (
        round(rightDrone[1].get("Lat"), 6),
        round(rightDrone[1].get("Lon"), 6),
        round((rightDrone[1].get("aAlt") + rightOffset), 6),
    )
    moveToCoordinate(baseStation, rightTargetCoordinate, rightDrone[0])

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(
            waitForMovementToComplete(
                baseStation, leftTargetCoordinate, leftDrone[0], "left"
            )
        ),
        loop.create_task(
            waitForMovementToComplete(
                baseStation, rightTargetCoordinate, rightDrone[0], "right"
            )
        ),
    ]
    loop.run_until_complete(asyncio.wait(tasks))

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

    # Find the drone with the largest Latitude() and make it the right drone
    # 'lambda item:item[1]["Lat"]' returns the latitude for each item in the coordinate list
    leftDrone = max(coordinateList, key=lambda item: item[1].get("Lat"))
    # Find the drone with the smallest Latitude() and make it the left drone
    rightDrone = min(coordinateList, key=lambda item: item[1].get("Lat"))

    # Leftover drone is the middle drone
    for droneTuple in coordinateList:
        if droneTuple is not leftDrone and droneTuple is not rightDrone:
            middleDrone = droneTuple

    print(f"left drone: {leftDrone[0].droneHumanName}")
    print(f"middle drone: {middleDrone[0].droneHumanName}")
    print(f"right drone: {rightDrone[0].droneHumanName}")

    try:
        currentFormation = baseStation.getCurrentFormation()
        if currentFormation.get("formationType") == "3Line":
            print("Drones already in Horizontal Line formation")
            return leftDrone, middleDrone, rightDrone
    except:
        pass

    global start_time
    start_time = time.time()

    # Change the left drone latitude to -0.00003 from the middleDrone
    # Change the right drone latitude to +0.00003 from the middleDrone
    print("left drone +0.00003 start--- %s seconds ---" % (time.time() - start_time))
    print("right drone -0.00003 start--- %s seconds ---" % (time.time() - start_time))
    leftDrone, rightDrone = adjustLat(
        baseStation,
        leftDrone,
        rightDrone,
        round((middleDrone[1].get("Lat") + 0.00003 - leftDrone[1].get("Lat")), 6),
        round((middleDrone[1].get("Lat") - 0.00003 - rightDrone[1].get("Lat")), 6),
    )

    # Get all the drones to the same longitude (middle drone longitude)
    print("left drone long start--- %s seconds ---" % (time.time() - start_time))
    print("right drone long start--- %s seconds ---" % (time.time() - start_time))
    leftDrone, rightDrone = adjustLon(
        baseStation,
        leftDrone,
        rightDrone,
        round((middleDrone[1].get("Lon") - leftDrone[1].get("Lon")), 6),
        round((middleDrone[1].get("Lon") - rightDrone[1].get("Lon")), 6),
    )

    # Get all the drones to the same altitude (middle drone altitude)
    print("left drone alt start--- %s seconds ---" % (time.time() - start_time))
    print("right drone alt start--- %s seconds ---" % (time.time() - start_time))
    leftDrone, rightDrone = adjustAlt(
        baseStation,
        leftDrone,
        rightDrone,
        round((middleDrone[1].get("aAlt") - leftDrone[1].get("aAlt")), 6),
        round((middleDrone[1].get("aAlt") - rightDrone[1].get("aAlt")), 6),
    )

    currentFormation = {
        "formationType": "3Line",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": 0,
        "expansionFactor": 1,
    }
    baseStation.setCurrentFormation(currentFormation)

    return leftDrone, middleDrone, rightDrone


def formHorizontalTriangleThreeDrones(baseStation):
    try:
        currentFormation = baseStation.getCurrentFormation()
        if currentFormation.get("formationType") == "3Triangle":
            print("Drones already in Horizontal Triangle formation")
            return
    except:
        pass

    leftDrone, middleDrone, rightDrone = formHorizontalLineThreeDrones(baseStation)

    # move the leftDrone and rightDrone backwards
    leftDrone, rightDrone = adjustLon(
        baseStation, leftDrone, rightDrone, -0.00003, -0.00003
    )

    currentFormation = {
        "formationType": "3Triangle",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": 0,
        "expansionFactor": 1,
    }
    baseStation.setCurrentFormation(currentFormation)

    return leftDrone, middleDrone, rightDrone


def rotateSwarm(baseStation):
    # rotates a swarm of 3 drones, depending on what formation they are currently in
    currentFormation = baseStation.getCurrentFormation()

    if currentFormation is None:
        print("No formation has been created yet")
        return

    formationType = currentFormation.get("formationType")
    droneTuple = currentFormation.get("droneTuple")
    rotation = currentFormation.get("rotation")
    currentExpansionFactor = currentFormation.get("expansionFactor")

    formationOptions = {
        "3Line": horizontalLineRotate,
        "3Triangle": horizontalTriangleRotate,
    }

    if formationType in formationOptions:
        # Returns new formation object
        formation = formationOptions[formationType](
            baseStation, droneTuple, rotation, currentExpansionFactor
        )
    else:
        print(f"Formation {formationType} is unknown")
        formation = None

    baseStation.setCurrentFormation(formation)


def horizontalLineRotate(baseStation, droneTuple, rotation, currentExpansionFactor):

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

    if order == 1:
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            lonMult * 0.00003 * currentExpansionFactor,
            -lonMult * 0.00003 * currentExpansionFactor,
        )
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            -latMult * 0.00003 * currentExpansionFactor,
            latMult * 0.00003 * currentExpansionFactor,
        )
    else:
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            -latMult * 0.00003 * currentExpansionFactor,
            latMult * 0.00003 * currentExpansionFactor,
        )
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            lonMult * 0.00003 * currentExpansionFactor,
            -lonMult * 0.00003 * currentExpansionFactor,
        )

    newFormation = {
        "formationType": "3Line",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": (rotation + 90) % 360,
        "expansionFactor": currentExpansionFactor,
    }

    return newFormation


def horizontalTriangleRotate(baseStation, droneTuple, rotation, currentExpansionFactor):

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

    if order == 1:
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            lonMult * 0.00006 * currentExpansionFactor,
            0,
        )
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            0,
            latMult * 0.00006 * currentExpansionFactor,
        )
    else:
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            -latMult * 0.00006 * currentExpansionFactor,
            0,
        )
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            0,
            -lonMult * 0.00006 * currentExpansionFactor,
        )

    newFormation = {
        "formationType": "3Triangle",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": (rotation + 90) % 360,
        "expansionFactor": currentExpansionFactor,
    }

    return newFormation


def expandSwarm(baseStation):
    # expands the swarm by double the current size
    currentFormation = baseStation.getCurrentFormation()

    if currentFormation is None:
        print("No formation has been created yet")
        return

    formationType = currentFormation.get("formationType")
    droneTuple = currentFormation.get("droneTuple")
    rotation = currentFormation.get("rotation")
    currentExpansionFactor = currentFormation.get("expansionFactor")

    formationOptions = {
        "3Line": horizontalLineExpand,
        "3Triangle": horizontalTriangleExpand,
    }

    if formationType in formationOptions:
        # Returns new formation object
        formation = formationOptions[formationType](
            baseStation, droneTuple, rotation, currentExpansionFactor
        )
    else:
        print(f"Formation {formationType} is unknown")
        formation = None

    baseStation.setCurrentFormation(formation)


def horizontalLineExpand(baseStation, droneTuple, rotation, currentExpansionFactor):

    leftDrone, middleDrone, rightDrone = droneTuple

    # Double the expansion
    newExpansionFactor = currentExpansionFactor

    rotationControl = {
        0: (1, 1, 1),
        90: (0, 1, -1),
        180: (1, -1, -1),
        270: (0, -1, 1),
    }

    order, latMult, lonMult = rotationControl[rotation]

    if order == 1:  # Drones are lined up on the same longitude
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            latMult * 0.00003 * newExpansionFactor,
            -latMult * 0.00003 * newExpansionFactor,
        )
    else:  # Drones are lined up on the same latitude
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            lonMult * 0.00003 * newExpansionFactor,
            -lonMult * 0.00003 * newExpansionFactor,
        )

    newFormation = {
        "formationType": "3Line",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": rotation,
        "expansionFactor": 2 * newExpansionFactor,
    }

    return newFormation


def horizontalTriangleExpand(baseStation, droneTuple, rotation, currentExpansionFactor):

    leftDrone, middleDrone, rightDrone = droneTuple

    newExpansionFactor = currentExpansionFactor

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

    if order == 1:  # Back drones are lined up on the same longitude
        # Increase the latitude difference (double)
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            latMult * 0.00003 * newExpansionFactor,
            -latMult * 0.00003 * newExpansionFactor,
        )
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            -lonMult * 0.00003 * newExpansionFactor,
            -lonMult * 0.00003 * newExpansionFactor,
        )
    else:  # back drones are lined up on the same latitude
        # Increase the longitude difference (double)
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            -lonMult * 0.00003 * newExpansionFactor,
            lonMult * 0.00003 * newExpansionFactor,
        )
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            latMult * 0.00003 * newExpansionFactor,
            latMult * 0.00003 * newExpansionFactor,
        )

    newFormation = {
        "formationType": "3Triangle",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": rotation,
        "expansionFactor": 2 * newExpansionFactor,
    }

    return newFormation


def retractSwarm(baseStation):
    # retracts the swarm by half the current size
    currentFormation = baseStation.getCurrentFormation()
    if currentFormation is None:
        print("No formation has been created yet")
        return

    formationType = currentFormation.get("formationType")
    droneTuple = currentFormation.get("droneTuple")
    rotation = currentFormation.get("rotation")
    currentExpansionFactor = currentFormation.get("expansionFactor")

    if currentExpansionFactor == 1:
        print("Cannot retract the swarm any further")
        return

    formationOptions = {
        "3Line": horizontalLineRetract,
        "3Triangle": horizontalTriangleRetract,
    }

    if formationType in formationOptions:
        # Returns new formation object
        formation = formationOptions[formationType](
            baseStation, droneTuple, rotation, currentExpansionFactor
        )
    else:
        print(f"Formation {formationType} is unknown")
        formation = None

    baseStation.setCurrentFormation(formation)


def horizontalLineRetract(baseStation, droneTuple, rotation, currentExpansionFactor):
    leftDrone, middleDrone, rightDrone = droneTuple

    # move the drones back one expansion factor
    newExpansionFactor = currentExpansionFactor / 2

    rotationControl = {
        0: (1, 1, 1),
        90: (0, 1, -1),
        180: (1, -1, -1),
        270: (0, -1, 1),
    }

    order, latMult, lonMult = rotationControl[rotation]

    if order == 1:  # Drones are lined up on the same longitude
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            -latMult * 0.00003 * newExpansionFactor,
            latMult * 0.00003 * newExpansionFactor,
        )
    else:  # Drones are lined up on the same latitude
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            -lonMult * 0.00003 * newExpansionFactor,
            lonMult * 0.00003 * newExpansionFactor,
        )

    newFormation = {
        "formationType": "3Line",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": rotation,
        "expansionFactor": newExpansionFactor,
    }

    return newFormation


def horizontalTriangleRetract(
    baseStation, droneTuple, rotation, currentExpansionFactor
):
    leftDrone, middleDrone, rightDrone = droneTuple

    newExpansionFactor = currentExpansionFactor / 2

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

    if order == 1:  # Back drones are lined up on the same longitude
        # Increase the latitude difference (double)
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            -latMult * 0.00003 * newExpansionFactor,
            latMult * 0.00003 * newExpansionFactor,
        )
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            lonMult * 0.00003 * newExpansionFactor,
            lonMult * 0.00003 * newExpansionFactor,
        )
    else:  # back drones are lined up on the same latitude
        # Increase the longitude difference (double)
        leftDrone, rightDrone = adjustLon(
            baseStation,
            leftDrone,
            rightDrone,
            lonMult * 0.00003 * newExpansionFactor,
            -lonMult * 0.00003 * newExpansionFactor,
        )
        leftDrone, rightDrone = adjustLat(
            baseStation,
            leftDrone,
            rightDrone,
            -latMult * 0.00003 * newExpansionFactor,
            -latMult * 0.00003 * newExpansionFactor,
        )

    newFormation = {
        "formationType": "3Triangle",
        "droneTuple": (leftDrone, middleDrone, rightDrone),
        "rotation": rotation,
        "expansionFactor": newExpansionFactor,
    }

    return newFormation
