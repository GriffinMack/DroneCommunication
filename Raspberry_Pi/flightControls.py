import time
import asyncio
import json

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
        "manual control": manualControl,
    }
    # Check for any additional info in the command (should be split by a :)
    try:
        incomingMessage, additionalInfo = incomingMessage.split(":")
    except:
        additionalInfo = None
    return flightControls.get(incomingMessage, default)(droneDevice, additionalInfo)


def getDroneCoordinates(droneDevice, additionalInfo=None):
    # Send gps info to base station
    # TODO: Send import info back to base station through the zigbee
    async def run():
        pixhawkDevice = droneDevice.getPixhawkDevice()
        pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()
        print("Collecting Drone Coordinates...")
        async for position in pixhawkVehicle.telemetry.position():
            absolute_altitude = position.absolute_altitude_m
            relative_altitude = position.relative_altitude_m
            latitude = position.latitude_deg
            longitude = position.longitude_deg
            break

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
        print(jsDroneCoordinates)
        return jsDroneCoordinates

    loop = asyncio.get_event_loop()
    jsDroneCoordinates = loop.run_until_complete(run())
    return jsDroneCoordinates



def getDroneSummary(droneDevice, additionalInfo=None):
    # Send drone summary info to base station
    # TODO: Send import info back to base station through the zigbee
    async def run():
        pixhawkDevice = droneDevice.getPixhawkDevice()
        pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()

        print("Collecting Drone Summary...")
        async for in_air in pixhawkVehicle.telemetry.in_air():
            inAirStatus = in_air
            break

        async for is_armed in pixhawkVehicle.telemetry.armed():
            isArmed = is_armed
            break

        async for gps_info in pixhawkVehicle.telemetry.gps_info():
            numSatellites = gps_info.num_satellites
            fixType = str(gps_info.fix_type)
            break

        async for battery in pixhawkVehicle.telemetry.battery():
            battery = battery.remaining_percent
            break

        async for flight_mode in pixhawkVehicle.telemetry.flight_mode():
            flightMode = str(flight_mode)
            break

        # Create dictionary for drone summary info
        droneSummary = {
            "In Air": inAirStatus,
            "Is Armed": isArmed,
            "Number of Satellites": numSatellites,
            "Fix Type": fixType,
            "Battery Remaining": battery,
            "Flight Mode": flightMode,
        }
        print(droneSummary)

        # Convert to json string
        jsDroneSummary = json.dumps(droneSummary)
        return jsDroneSummary

    loop = asyncio.get_event_loop()
    jsDroneSummary = loop.run_until_complete(run())
    return jsDroneSummary


def takeoffDrone(droneDevice, additionalInfo=None):
    async def run():
        pixhawkDevice = droneDevice.getPixhawkDevice()
        pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()

        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break
        try:
            print("-- Arming")
            await pixhawkVehicle.action.arm()

            print("-- Taking off")
            await pixhawkVehicle.action.takeoff()
        except Exception as e:
            print(e)

        # TODO: check that the drone has reached the takeoff altitude

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def landDrone(droneDevice, additionalInfo=None):
    async def run():
        pixhawkDevice = droneDevice.getPixhawkDevice()
        pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()

        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("-- Landing")
        try:
            await pixhawkVehicle.action.land()
        except Exception as e:
            print(e)

        # TODO: check that the drone has reached the ground

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def moveToCoordinates(droneDevice, additionalInfo=None):
    async def run():
        pixhawkDevice = droneDevice.getPixhawkDevice()
        pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()

        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("Fetching amsl altitude at home location....")
        async for terrain_info in pixhawkDevice.pixhawkVehicle.telemetry.home():

            # additional info slice is to cut out parentheses caused by tuple to str conversion
            lat, lon, alt = additionalInfo[1:-1].split(",")

            absolute_altitude = terrain_info.absolute_altitude_m + float(alt)
            latitude = terrain_info.latitude_deg + float(lat)
            longitude = terrain_info.longitude_deg + float(lon)

            break  # To break out of async so it doesn't loop continuously

        # Checks to see that drone is in air, although does not check minimum relative altitude as far as I know
        async for in_air in pixhawkDevice.pixhawkVehicle.telemetry.in_air():
            if not in_air:
                # TODO: Send this message back to the base station so they know it didnt work
                print("Not in air")
                return
            else:
                break

        await asyncio.sleep(1)
        flying_alt = absolute_altitude

        # goto_location() takes Absolute MSL altitude
        await pixhawkDevice.pixhawkVehicle.action.goto_location(
            latitude, longitude, flying_alt, 0
        )

        # TODO: Wait for the drone to reach the desired location

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def homeLocationHover(droneDevice, additionalInfo=None):
    async def run():
        pixhawkDevice = droneDevice.getPixhawkDevice()
        pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()

        # TODO: Check if the drone is actually in the air
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
        flying_alt = absolute_altitude + 3.0  # To hover drone 10m above ground

        # goto_location() takes Absolute MSL altitude
        await pixhawkVehicle.action.goto_location(latitude, longitude, flying_alt, 0)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def followBaseStation(droneDevice, additionalInfo=None):
    pass


def manualControl(droneDevice, additionalInfo=None):
    async def manual_controls():
        pixhawkDevice = droneDevice.getPixhawkDevice()
        pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()

        xbeeDevice = droneDevice.getXbeeDevice()
        # This waits till a mavlink based drone is connected
        async for state in pixhawkVehicle.core.connection_state():
            if state.is_connected:
                print(f"-- Connected to drone with UUID: {state.uuid}")
                break

        # Checking if Global Position Estimate is ok
        async for global_lock in pixhawkVehicle.telemetry.health():
            if global_lock.is_global_position_ok:
                print("-- Global position state is ok")
                break

        # set the manual control input before arming
        await pixhawkVehicle.manual_control.set_manual_control_input(
            float(0), float(0), float(0.5), float(0)
        )
        try:
            # Arming the drone
            print("-- Arming")
            await pixhawkVehicle.action.arm()
        except:
            # TODO: change this from a general exception to a specific one
            print("vehicle already armed")

        # set the manual control input after arming
        await pixhawkVehicle.manual_control.set_manual_control_input(
            float(0), float(0), float(0.5), float(0)
        )

        # start manual control
        print("-- Starting manual control")
        await pixhawkVehicle.manual_control.start_position_control()

        # list of possible manual controls
        # TODO: Simulator movement is a bit fast, maybe lower these values a bit
        manualControls = {
            "up": [0, 0, 1, 0],  # throttle max
            "down": [0, 0, 0, 0],  # throttle min
            "left": [0, -0.5, 0.5, 0],  # yaw min
            "right": [0, 0.5, 0.5, 0],  # yaw max
            "left rotate": [0, 0, 0.5, -0.5],  # pitch min
            "right rotate": [0, 0, 0.5, 0.5],  # pitch max
            "forward": [0.5, 0, 0.5, 0],  # roll max
            "backward": [-0.5, 0, 0.5, 0],  # roll min
        }
        while True:
            # check for a xbee message
            message = xbeeDevice.checkForIncomingMessage()

            # default to no movement
            manualControlsInput = [0, 0, 0.5, 0]
            if message in manualControls:
                manualControlsInput = manualControls[message]

            await pixhawkVehicle.manual_control.set_manual_control_input(
                *map(float, manualControlsInput)
            )

            await asyncio.sleep(0.05)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(manual_controls())

def default(droneDevice, additionalInfo=None):
    print("Incorrect syntax")
