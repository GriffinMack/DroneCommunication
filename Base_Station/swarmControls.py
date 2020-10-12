

def horizontalLine(baseStationXbeeDevice, droneDevice=None):
    print("making horizontal line..")

    leaderGPS = (0, 0 , -1)

    if droneDevice is not None
    	leaderGPS = json.load(gpsData(baseStationXbeeDevice, droneDevice))

    for drone in baseStationXbeeDevice.remoteDroneList
    	mult = -1 ** drone.index() # alternate between moving other drones up and down

    	# TODO: Add collision avoidance for drones being above
    	# Need to get current drone object's GPS to move better proof of concept

    	coordinate = (0, 0, (mult * 2))
    	moveFromCurrent(baseStationXbeeDevice, coordinate, drone)

    for drone in baseStationXbeeDevice.remoteDroneList
    	mult = -1 ** drone.index()

    	coordinate = (leaderGPS["Lat"], leaderGPS["Lon"] + (mult * drone.index() * 2), leaderGPS["aAlt"] + (mult * 2))
    	moveToCoordinate(baseStationXbeeDevice, coordinate, drone)

    	coordinate = (0, 0, (mult * -2))
    	moveFromCurrent(baseStationXbeeDevice, coordinate, drone)



def horizontalTriangle(baseStationXbeeDevice, droneDevice=None):
    print("making horizontal triangle..")
	

