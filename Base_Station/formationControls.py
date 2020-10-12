# Griffin Mack
# 9/21/2020
#
# Functions meant to form a formation with multiple drones
#
#
from devices import BaseStation
from flightControls import gpsData, moveFromCurrent, moveToCoordinate


def formHorizontalLineThreeDrones(baseStation):
    print("Forming a horizontal line with three drones..")

    # gather all the discovered drone coordinates
    droneList = baseStation.getRemoteDroneList()
    coordinateList = []
    for drone in droneList:
        droneCoordinates = gpsData(baseStation, drone)
        coordinateList.append((drone, droneCoordinates))

    # Find the drone with the largest Latitude() and make it the left drone
    # 'lambda item:item[1]["Lat"]' returns the latitude for each item in the coordinate list
    leftDrone = max(coordinateList, key=lambda item: item[1].get("Lat"))
    # Find the drone with the smallest Latitude() and make it the right drone
    rightDrone = min(coordinateList, key=lambda item: item[1].get("Lat"))

    # Leftover drone is the middle drone
    for droneTuple in coordinateList:
        if droneTuple is not leftDrone or rightDrone:
            middleDrone = droneTuple

    # Change the left drone latitude to -0.00003 from the middleDrone
    moveToCoordinate(
        baseStation,
        (
            middleDrone[1].get("Lat") - 0.00003,
            leftDrone[1].get("Lon"),
            leftDrone[1].get("aAlt"),
        ),
        leftDrone[0],
    )
    # Change the right drone latitude to +0.00003 from the middleDrone
    moveToCoordinate(
        baseStation,
        (
            middleDrone[1].get("Lat") + 0.00003,
            rightDrone[1].get("Lon"),
            rightDrone[1].get("aAlt"),
        ),
        rightDrone[0],
    )
    # Get all the drones to the same longitude
    moveToCoordinate(
        baseStation,
        (leftDrone[1].get("Lat"), middleDrone[1].get("Lon"), leftDrone[1].get("aAlt")),
        leftDrone[0],
    )
    moveToCoordinate(
        baseStation,
        (
            rightDrone[1].get("Lat"),
            middleDrone[1].get("Lon"),
            rightDrone[1].get("aAlt"),
        ),
        rightDrone[0],
    )
    # Get all the drones to the same altitude
    moveToCoordinate(
        baseStation,
        (leftDrone[1].get("Lat"), leftDrone[1].get("Lon"), middleDrone[1].get("aAlt")),
        leftDrone[0],
    )
    moveToCoordinate(
        baseStation,
        (
            rightDrone[1].get("Lat"),
            rightDrone[1].get("Lon"),
            middleDrone[1].get("aAlt"),
        ),
        rightDrone[0],
    )
    return leftDrone, middleDrone, rightDrone


def formHorizontalTriangleThreeDrones(baseStation):
    leftDrone, middleDrone, rightDrone = formHorizontalLine(baseStation)
    # move the leftDrone and rightDrone backwards
    moveFromCurrent(baseStation, (0, -0.00003, 0), leftDrone[0])
    moveFromCurrent(baseStation, (0, -0.00003, 0), rightDrone[0])
