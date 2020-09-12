import time
import asyncio

from mavsdk.geofence import Point, Polygon


def decodeMessage(droneDevice, incomingMessage):
    # takes an incoming message and finds a flight control that corresponds
    flightControls = {
        "takeoff": takeoffDrone,
        "land": landDrone,
        "move to coordinate": moveToCoordinates,
        "return to home without landing": homeLocationHover,
        "follow me": followBaseStation,
        "debug": getDroneSummary,
        "gps": getDroneCoordinates,
        "up": manuallyMoveDroneUp,
        "left rotate": manuallyRotateDroneLeft,
        "right rotate": manuallyRotateDroneRight,
        "down": manuallyMoveDroneDown,
        "forward": manuallyMoveDroneForward,
        "backward": manuallyMoveDroneBackward,
        "left": manuallyMoveDroneLeft,
        "right": manuallyMoveDroneRight,
    }
    # Check for any additional info in the command (should be split by a :)
    try:
        incomingMessage, additionalInfo = incomingMessage.split(':')
    except:
        additionalInfo = None
    return flightControls[incomingMessage](droneDevice.pixhawkDevice, additionalInfo)


def getDroneCoordinates(pixhawkDevice, additionalInfo=None):
    pass
    # TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call

    # TODO: Take the most helpful items and send them back to the base station through the Zigbee (find an efficient way to do this. We don't want to send 20 different messages just for basic info. Maybe combine everything into one string and break it back up on the other end)


def getDroneSummary(pixhawkDevice, additionalInfo=None):
    pass
    # TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call

    # TODO: Take the most helpful items and send them back to the base station through the Zigbee (find an efficient way to do this. We don't want to send 20 different messages just for basic info. Maybe combine everything into one string and break it back up on the other end)


def takeoffDrone(pixhawkDevice, additionalInfo=None):
    async def run():
        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkDevice.pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break
        try:
            print("-- Arming")
            await pixhawkDevice.pixhawkVehicle.action.arm()

            print("-- Taking off")
            await pixhawkDevice.pixhawkVehicle.action.takeoff()
        except Exception as e:
            print(e)

        # TODO: check that the drone has reached the takeoff altitude

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def landDrone(pixhawkDevice, additionalInfo=None):
    async def run():
        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkDevice.pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("-- Landing")
        try:
            await pixhawkDevice.pixhawkVehicle.action.land()
        except Exception as e:
            print(e)

        # TODO: check that the drone has reached the ground

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def moveToCoordinates(pixhawkDevice, additionalInfo=None):
    async def run():
        # TODO: Get the user inputted coordinates from the XBEE message
        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkDevice.pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("Fetching amsl altitude at home location....")
        async for terrain_info in pixhawkDevice.pixhawkVehicle.telemetry.home():
            absolute_altitude = terrain_info.absolute_altitude_m
            latitude = terrain_info.latitude_deg
            longitude = terrain_info.longitude_deg
            break

        # TODO: Check if the drone is actually in the air

        await asyncio.sleep(1)
        flying_alt = absolute_altitude + 20.0  # To fly drone 20m above the ground plane

        # goto_location() takes Absolute MSL altitude
        await pixhawkDevice.pixhawkVehicle.action.goto_location(
            latitude + 0.0002, longitude + 0.0002, flying_alt, 0
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def homeLocationHover(pixhawkDevice, additionalInfo=None):
    async def run():
        # TODO: Check if the drone is actually in the air
        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkDevice.pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("Fetching amsl altitude at home location....")
        async for terrain_info in pixhawkDevice.pixhawkVehicle.telemetry.home():
            absolute_altitude = terrain_info.absolute_altitude_m
            latitude = terrain_info.latitude_deg
            longitude = terrain_info.longitude_deg
            break

        await asyncio.sleep(1)
        flying_alt = absolute_altitude + 10.0  # To hover drone 10m above ground

        # goto_location() takes Absolute MSL altitude
        await pixhawkDevice.pixhawkVehicle.action.goto_location(
            latitude, longitude, flying_alt, 0
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def followBaseStation(pixhawkDevice, additionalInfo=None):
    pass


# TODO: All of these functions can utilize the ManualControl class of mavsdk
def manuallyMoveDroneUp(pixhawkDevice, additionalInfo=None):
    print("moving drone left")
    # Z +1


def manuallyRotateDroneLeft(droneDevice, additionalInfo=None):
    print("moving drone left")
    # r -1


def manuallyRotateDroneRight(droneDevice, additionalInfo=None):
    print("moving drone right")
    # r +1


def manuallyMoveDroneDown(droneDevice, additionalInfo=None):
    print("moving drone down")
    # Z -1


def manuallyMoveDroneForward(droneDevice, additionalInfo=None):
    print("moving drone forward")
    # X +1


def manuallyMoveDroneBackward(droneDevice, additionalInfo=None):
    print("moving drone backward")
    # X -1


def manuallyMoveDroneLeft(droneDevice, additionalInfo=None):
    print("moving drone left")
    # Y -1


def manuallyMoveDroneRight(droneDevice, additionalInfo=None):
    print("moving drone right")
    # Y +1


def establishGeofence(pixhawkDevice):
    async def run():
        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkDevice.pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("Fetching amsl altitude at home location....")
        async for terrain_info in pixhawkDevice.pixhawkVehicle.telemetry.home():
            absolute_altitude = terrain_info.absolute_altitude_m
            latitude = terrain_info.latitude_deg
            longitude = terrain_info.longitude_deg
            break

        await asyncio.sleep(1)

        p1 = Point(latitude - 0.00001, longitude - 0.00001)
        p2 = Point(latitude + 0.00001, longitude - 0.00001)
        p3 = Point(latitude + 0.00001, longitude + 0.00001)
        p4 = Point(latitude - 0.00001, longitude + 0.00001)

        polygon = Polygon([p1, p2, p3, p4], Polygon.FenceType.INCLUSION)

        print("-- Uploading geofence")
        await pixhawkDevice.pixhawkVehicle.geofence.upload_geofence([polygon])

        # TODO: The geofence uploads but nothing happens when it is violated. Check ISSUE #255 on MAVSDK-PYTHON

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())