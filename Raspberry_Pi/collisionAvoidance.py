from flightControls import getDroneCoordinates

import json
import asyncio


def establishGeofence(droneDevice):
    async def run():
        pixhawkDevice = droneDevice.getPixhawkDevice()
        pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()
        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("Fetching amsl altitude at home location....")
        async for terrain_info in pixhawkVehicle.telemetry.home():
            absolute_altitude = terrain_info.absolute_altitude_m
            latitude = terrain_info.latitude_deg
            longitude = terrain_info.longitude_deg
            break

        await asyncio.sleep(1)

        p1 = Point(latitude - 0.0001, longitude - 0.0001)
        p2 = Point(latitude + 0.0001, longitude - 0.0001)
        p3 = Point(latitude + 0.0001, longitude + 0.0001)
        p4 = Point(latitude - 0.0001, longitude + 0.0001)

        polygon = Polygon([p1, p2, p3, p4], Polygon.FenceType.INCLUSION)

        print("-- Uploading geofence")
        await pixhawkVehicle.geofence.upload_geofence([polygon])

        # TODO: The geofence uploads but nothing happens when it is violated. Check ISSUE #255 on MAVSDK-PYTHON

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def localCollisionAvoidance(droneDevice):
    # Should be called any time the drone is in motion
    xbeeDevice = droneDevice.getXbeeDevice()
    currentLocation = getDroneCoordinates(droneDevice)

    # Broadcasts the drone's GPS location to any drones in the area
    xbeeDevice.sendMessage(currentLocation)


def checkIncomingLocation(droneDevice, incomingLocation):
    # Check the location and see if it is too close to the local drone
    # Incoming location: {'Latitude (degrees)': 47.3977418, 'Longitude (degrees)': 8.545594099999999, 'Relative Altitude (m)': 0.0020000000949949026, 'Absolute Altitude (m)': 488.010009765625}
    remoteLocationDict = json.loads(incomingLocation)
    localLocationDict = json.loads(getDroneCoordinates(droneDevice))

    localLocation = [
        localLocationDict["Latitude (degrees)"],
        localLocationDict["Longitude (degrees)"],
    ]
    incomingLocation = [
        incomingLocationDict["Latitude (degrees)"],
        localLocationDict["Longitude (degrees)"],
    ]

    map(float, localLocation)
    map(float, incomingLocation)

    distanceApart = geodesic(localLocation, incomingLocation).meters

    if distanceApart < droneDevice.getSafeDistance():
        # check if the altitudes are different (start with 5 meters)
        print("Drone's GPS location close. Checking Altitude..")
        localAltitude = float(localLocationDict["Absolute Altitude (m)"])
        incomingAltitude = float(incomingLocationDict["Absolute Altitude (m)"])

        altitudeDistance = abs(localAltitude - incomingAltitude)
        
        if altitudeDistance < droneDevice.getSafeAltitudeDistance():
            print("TOO CLOSE")
