import asyncio
import time
import json

from mavsdk.geofence import Point, Polygon
from geopy.distance import geodesic
from flightControls import getDroneCoordinates


async def collisionAvoidanceBroadcastCheck(droneDevice):
    # Checks if the drone needs to broadcast its location (broadcast if the drone is moving)
    i = 1
    droneMoving = False
    pixhawkVehicle = droneDevice.getPixhawkVehicle()
    print("-- Starting collision avoidance..")
    async for position in pixhawkVehicle.telemetry.position_velocity_ned():
        velocitiesDict = vars(position.velocity)
        for velocity in velocitiesDict.values():
            if abs(float(velocity)) > 0.5:
                droneMoving = True
            else:
                droneMoving = False
        print(f"{i}. {droneMoving}")
        if droneMoving is True:
            # The drone is moving, send the gps location out
            await droneDevice.sendMessage(droneDevice.getCurrentPosition())
        i = i + 1

async def updateDroneCoordinate(droneDevice):
    # Constantly updates the 
    pixhawkVehicle = droneDevice.getPixhawkVehicle()
    i = 1
    print("-- Starting Coordinate Collection...")
    async for position in pixhawkVehicle.telemetry.position():
        absolute_altitude = position.absolute_altitude_m
        relative_altitude = position.relative_altitude_m
        latitude = position.latitude_deg
        longitude = position.longitude_deg
        # Put coordinates into a dictionary and send off as json string
        droneCoordinates = {
            "Lat": latitude,
            "Lon": longitude,
            "rAlt": relative_altitude,
            "aAlt": absolute_altitude,
        } 
        # Round the numbers so we don't exceed xbee byte limit
        for coord in droneCoordinates:
            rounded = round(droneCoordinates[coord], 5)
            droneCoordinates[coord] = rounded

        # Convert to json string
        jsDroneCoordinates = json.dumps(droneCoordinates)

        # Update the objects current position
        droneDevice.setCurrentPosition(jsDroneCoordinates)
        print(f"{i}. updated coordinate")
        i = i + 1



def establishGeofence(droneDevice):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()
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
