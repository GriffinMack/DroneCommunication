# Griffin Mack
# 9/21/2020
#
# Functions meant to form a formation with multiple drones
#
#
from devices import BaseStation
from flightControls import gpsData, moveFromCurrent, moveToCoordinate


def formHorizontalLine(baseStation):
    print("Forming a horizontal line..")

    # rediscover the network
    # baseStation.rediscoverConnectedDrones()

    # check that stanley is in the network
    droneList = baseStation.getRemoteDroneList()
    if "Stanley" not in droneList:
        print("ERROR: Stanley not found, exiting formation control")
        return None

    # remove stanley from the drone list (store it in a variable)
    for drone in droneList:
        if drone.getDroneName() == "Stanley":
            stanleyDrone = drone
            droneList.remove(drone)

    # TODO: Check that all drones are stationary (formations shouldnt be made if not)

    # get the gps coordinates for Stanley
    stanleyCoordinates = gpsData(baseStation, stanleyDrone)
    stanleyLat = stanleyCoordinates["lat"]
    stanleyLong = stanleyCoordinates["lon"]
    stanleyAlt = stanleyCoordinates["alt"]

    # move the drones to the same altitude
    for drone in droneList:
        coordinate = (0, 0, stanleyAlt)
        moveToCoordinate(baseStation, coordinate, drone)
    
    # TODO: Check if there was any collisions detected. If so, skip the next step

    # move the drones to different alitudes
    moveFromCurrent(baseStation, (0, 0, -5), droneList[0])
    moveFromCurrent(baseStation, (0, 0, 5), droneList[1])

    # move the drones into a horizontal line on different altitudes(north to south, with stanley in the middle)
    moveToCoordinate(baseStation, (stanleyLat + 0.00003, stanleyLong, 0), droneList[0])
    moveToCoordinate(baseStation, (stanleyLat - 0.00003, stanleyLong, 0), droneList[1])

    # move the drones into a horizontal line on the same altitude
    moveFromCurrent(baseStation, (0, 0, 5), droneList[0])
    moveFromCurrent(baseStation, (0, 0, -5), droneList[1])

    return droneList

def formHorizontalTriangle(baseStation):
    droneList = formHorizontalLine(baseStation)
    if droneList is None:
        return
    moveFromCurrent(baseStation, (0,-0.00003,0), droneList[0])
    moveFromCurrent(baseStation, (0,-0.00003,0), droneList[1])

def formVerticalLine(baseStation):
    pass

def formVerticalTriangle(baseStation):
    pass
