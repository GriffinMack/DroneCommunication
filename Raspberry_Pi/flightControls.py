import time
import asyncio
import json


def decodeMessage(droneDevice, incomingMessage):
    # takes the incoming message and finds a flight control that corresponds
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


def getDroneCoordinates(pixhawkDevice, additionalInfo = None):
    # Send gps info to base station
    # TODO: Send import info back to base station through the zigbee
    async def run():
        print("Collecting Drone Coordinates...")
        async for position in pixhawkDevice.pixhawkVehicle.telemetry.position():
            absolute_altitude = position.absolute_altitude_m
            relative_altitude = position.relative_altitude_m
            latitude = position.latitude_deg
            longitude = position.longitude_deg

            # Put coordinates into a dictionary and send off as json string
            droneCoordinates = {
                "Latitude (degrees)" : latitude,
                "Longitude (degrees)" : longitude,
                "Relative Altitude (m)" : relative_altitude,
                "Absolute Altitude (m)" : absolute_altitude
            }
            print(droneCoordinates)

            # Convert to json string
            jsDroneCoordinates = json.dumps(droneCoordinates)
            return jsDroneCoordinates      

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def getDroneSummary(pixhawkDevice, additionalInfo = None):
    # Send drone summary info to base station
    # TODO: Send import info back to base station through the zigbee
    async def run():
        print("Collecting Drone Summary...")        
        async for in_air in pixhawkDevice.pixhawkVehicle.telemetry.in_air():
            inAirStatus = in_air
            break

        async for is_armed in pixhawkDevice.pixhawkVehicle.telemetry.armed():
            isArmed = is_armed
            break
    
        async for gps_info in pixhawkDevice.pixhawkVehicle.telemetry.gps_info():
            numSatellites = gps_info.num_satellites
            fixType = str(gps_info.fix_type) # Converts enum to str type
            break
    
        async for battery in pixhawkDevice.pixhawkVehicle.telemetry.battery():
            battery = battery.remaining_percent
            break

        async for flight_mode in pixhawkDevice.pixhawkVehicle.telemetry.flight_mode():
            flightMode = str(flight_mode) # Converts enum to str type

            # Create dictionary for drone summary info
            droneSummary = {
                "In Air" : inAirStatus,
                "Is Armed" : isArmed,
                "Number of Satellites" : numSatellites,
                "Fix Type" : fixType,
                "Battery Remaining" : battery,
                "Flight Mode" : flightMode
            }
            print(droneSummary)

            # Convert to json string
            jsDroneSummary = json.dumps(droneSummary)
            return jsDroneSummary

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


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
