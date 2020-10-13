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


def waitForMovementToComplete(baseStation, targetCoordinate, droneDevice):
    targetLat = targetCoordinate[0]
    targetLon = targetCoordinate[1]
    targetAlt = targetCoordinate[2]

    currentGPSLocation = gpsData(baseStation, droneDevice)
    currentLat = currentGPSLocation["Lat"]
    currentLon = currentGPSLocation["Lon"]
    currentAlt = currentGPSLocation["aAlt"]

    # Check if the coordinate is close to the target (will vary by about 0.5m max)
    while (
        isclose(currentLat, targetLat, abs_tol=5e-6) is False
        or isclose(currentLon, targetLon, abs_tol=5e-6) is False
        or isclose(currentAlt, targetAlt, abs_tol=5e-1) is False
    ):
        print("Drone not close enough yet")
        time.sleep(0.5)
        currentGPSLocation = gpsData(baseStation, droneDevice)
        currentLat = currentGPSLocation["Lat"]
        currentLon = currentGPSLocation["Lon"]
        currentAlt = currentGPSLocation["aAlt"]
    print("DRONE CLOSE ENOUGH")


def getUpdatedDroneLocationTuple(baseStation, droneDevice):
    droneCoordinates = gpsData(baseStation, droneDevice)
    return (droneDevice, droneCoordinates)


def formHorizontalLineThreeDrones(baseStation):
    print("Forming a horizontal line with three drones..")

    # gather all the discovered drone coordinates
    droneList = baseStation.getRemoteDroneList()
    coordinateList = []
    for droneDevice in droneList:
        droneCoordinates = gpsData(baseStation, droneDevice)
        coordinateList.append((droneDevice, droneCoordinates))

    # Find the drone with the largest Latitude() and make it the left drone
    # 'lambda item:item[1]["Lat"]' returns the latitude for each item in the coordinate list
    leftDrone = max(coordinateList, key=lambda item: item[1].get("Lat"))
    print(leftDrone)
    # Find the drone with the smallest Latitude() and make it the right drone
    rightDrone = min(coordinateList, key=lambda item: item[1].get("Lat"))
    print(rightDrone)

    # Leftover drone is the middle drone
    for droneTuple in coordinateList:
        if droneTuple is not leftDrone or rightDrone:
            middleDrone = droneTuple
    print(middleDrone)
    # Change the left drone latitude to -0.00003 from the middleDrone
    targetCoordinate = (
        float(middleDrone[1].get("Lat")) - 0.00003,
        leftDrone[1].get("Lon"),
        leftDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0])
    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])

    # Change the right drone latitude to +0.00003 from the middleDrone
    targetCoordinate = (
        float(middleDrone[1].get("Lat")) + 0.00003,
        rightDrone[1].get("Lon"),
        rightDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    # Get all the drones to the same longitude
    targetCoordinate = (
        leftDrone[1].get("Lat"),
        middleDrone[1].get("Lon"),
        leftDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0])
    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat"),
        middleDrone[1].get("Lon"),
        rightDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    # Get all the drones to the same altitude
    targetCoordinate = (
        leftDrone[1].get("Lat"),
        leftDrone[1].get("Lon"),
        middleDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, leftDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0])
    leftDrone = getUpdatedDroneLocationTuple(baseStation, leftDrone[0])

    targetCoordinate = (
        rightDrone[1].get("Lat"),
        rightDrone[1].get("Lon"),
        middleDrone[1].get("aAlt"),
    )
    moveToCoordinate(baseStation, targetCoordinate, rightDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0])
    rightDrone = getUpdatedDroneLocationTuple(baseStation, rightDrone[0])

    return leftDrone, middleDrone, rightDrone


def formHorizontalTriangleThreeDrones(baseStation):
    leftDrone, middleDrone, rightDrone = formHorizontalLine(baseStation)
    # move the leftDrone and rightDrone backwards
    moveFromCurrent(baseStation, (0, -0.00003, 0), leftDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, leftDrone[0])

    moveFromCurrent(baseStation, (0, -0.00003, 0), rightDrone[0])
    waitForMovementToComplete(baseStation, targetCoordinate, rightDrone[0])
