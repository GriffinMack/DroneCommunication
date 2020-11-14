import time
import asyncio
import json

from mavsdk.geofence import Point, Polygon
from geopy.distance import geodesic


def decodeMessage(droneDevice, incomingMessage):
    # takes an incoming message and finds a flight control that corresponds
    flightControls = {
        "takeoff": takeoffDrone,
        "land": landDrone,
        "move to coordinate": moveToCoordinates,
        "move from home": moveFromHome,
        "move from current": moveFromCurrent,
        "return to home without landing": homeLocationHover,
        "set maximum speed": setMaximumSpeed,
        "follow me": followBaseStation,
        "debug": getDroneSummary,
        "gps": getDroneCoordinates,
        "manual control": manualControl,
    }
    # Check if the message is a GPS coordinate from another drone
    if incomingMessage[0] == "{" and incomingMessage.endswith("}"):
        checkIncomingLocation(droneDevice, incomingMessage)
        return None
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
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

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
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

        print("Collecting Drone Summary...")
        async for in_air in pixhawkVehicle.telemetry.in_air():
            inAirStatus = in_air
            break

        async for is_armed in pixhawkVehicle.telemetry.armed():
            isArmed = is_armed
            break

        async for battery in pixhawkVehicle.telemetry.battery():
            battery = battery.remaining_percent
            break

        async for flight_mode in pixhawkVehicle.telemetry.flight_mode():
            flightMode = str(flight_mode)
            break

        # Create dictionary for drone summary info
        droneSummary = {
            "Air": inAirStatus,
            "Arm": isArmed,
            "Bat": round(battery, 2),
            "Mode": flightMode,
        }

        # Convert to json string
        jsDroneSummary = json.dumps(droneSummary)
        print(jsDroneSummary)
        return jsDroneSummary

    loop = asyncio.get_event_loop()
    jsDroneSummary = loop.run_until_complete(run())

    return jsDroneSummary


def takeoffDrone(droneDevice, additionalInfo=None):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

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

            # Check if the user specified a takeoff altitude
            if additionalInfo:
                async for terrain_info in pixhawkVehicle.telemetry.home():
                    absolute_altitude = terrain_info.absolute_altitude_m + float(
                        additionalInfo
                    )
                    latitude = terrain_info.latitude_deg
                    longitude = terrain_info.longitude_deg
                    break
                await pixhawkVehicle.action.goto_location(
                    latitude, longitude, absolute_altitude, 0
                )
        except Exception as e:
            print(e)

        # TODO: check that the drone has reached the takeoff altitude

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def landDrone(droneDevice, additionalInfo=None):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

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


def statusText(droneDevice, additionalInfo=None):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

        print("Waiting for drone to have a global position estimate...")
        async for text in pixhawkVehicle.telemetry.status_text():
            print(text)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def moveToCoordinates(droneDevice, additionalInfo=None):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()
        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        # Takes input sent through XBee then splits it out into variables
        latitude, longitude, absolute_altitude = additionalInfo[1:-1].split(",")

        absolute_altitude = float(absolute_altitude)
        latitude = float(latitude)
        longitude = float(longitude)

        # Checks to see that drone is in air, although does not check minimum relative altitude as far as I know
        async for in_air in pixhawkVehicle.telemetry.in_air():
            if not in_air:
                print("Not in air")
                return
            else:
                break

        await asyncio.sleep(1)
        flying_alt = absolute_altitude

        # goto_location() takes Absolute MSL altitude
        await pixhawkVehicle.action.goto_location(latitude, longitude, flying_alt, 0)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def moveFromHome(droneDevice, additionalInfo=None):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("Fetching amsl altitude at home location....")
        async for terrain_info in pixhawkVehicle.telemetry.home():

            # additional info slice is to cut out parentheses caused by tuple to str conversion
            lat, lon, alt = additionalInfo[1:-1].split(",")

            absolute_altitude = terrain_info.absolute_altitude_m + float(alt)
            latitude = terrain_info.latitude_deg + float(lat)
            longitude = terrain_info.longitude_deg + float(lon)

            break  # To break out of async so it doesn't loop continuously

        # Checks to see that drone is in air, although does not check minimum relative altitude as far as I know
        async for in_air in pixhawkVehicle.telemetry.in_air():
            if not in_air:
                # TODO: Send this message back to the base station so they know it didnt work
                print("Not in air")
                return
            else:
                break

        await asyncio.sleep(1)
        flying_alt = absolute_altitude

        # goto_location() takes Absolute MSL altitude
        await pixhawkVehicle.action.goto_location(latitude, longitude, flying_alt, 0)

        # TODO: Wait for the drone to reach the desired location

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def moveFromCurrent(droneDevice, additionalInfo=None):
    # pixhawkDevice = droneDevice.getPixhawkDevice() Idk why this one was different so I'm leaving this in
    # pixhawkVehicle = pixhawkDevice.getPixhawkVehicle()

    pixhawkVehicle = droneDevice.getPixhawkVehicle()

    async def run():
        print("Waiting for drone to have a global position estimate...")
        async for health in pixhawkVehicle.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("Fetching amsl altitude at home location....")
        async for position in pixhawkVehicle.telemetry.position():

            # additional info slice is to cut out parentheses caused by tuple to str conversion
            try:
                lat, lon, alt = additionalInfo[1:-1].split(",")
            except:
                lat = 0
                lon = 0
                alt = 0

            # Uses current position data and formatted input from XBee to move drone
            absolute_altitude = position.absolute_altitude_m + float(alt)
            latitude = position.latitude_deg + float(lat)
            longitude = position.longitude_deg + float(lon)

            break  # To break out of async so it doesn't loop continuously

        # Checks to see that drone is in air, although does not check minimum relative altitude as far as I know
        async for in_air in pixhawkVehicle.telemetry.in_air():
            if not in_air:
                print("Not in air")
                return
            else:
                break

        await asyncio.sleep(1)
        flying_alt = absolute_altitude

        # goto_location() takes Absolute MSL altitude
        await pixhawkVehicle.action.goto_location(latitude, longitude, flying_alt, 0)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def homeLocationHover(droneDevice, additionalInfo=None):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

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


def setMaximumSpeed(droneDevice, newMaximumSpeed=None):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

        print("-- Setting Maximum Speed..")
        if newMaximumSpeed:
            try:
                await pixhawkVehicle.action.set_maximum_speed(float(newMaximumSpeed))
                print(f"successfully set maximum speed to {newMaximumSpeed}")
            except Exception as e:
                print(e)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def manualControl(droneDevice, additionalInfo=None):
    async def manual_controls():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()

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


def calibrateDevice(droneDevice):
    async def run():
        pixhawkVehicle = droneDevice.getPixhawkVehicle()
        print("-- Starting gyroscope calibration")
        async for progress_data in pixhawkVehicle.calibration.calibrate_gyro():
            print(progress_data)
        print("-- Gyroscope calibration finished")

        # TODO: The following commands require manual calibration. Test manually
        # print("-- Starting accelerometer calibration")
        # async for progress_data in pixhawkVehicle.calibration.calibrate_accelerometer():
        #     print(progress_data)
        # print("-- Accelerometer calibration finished")

        # print("-- Starting magnetometer calibration")
        # async for progress_data in pixhawkVehicle.calibration.calibrate_magnetometer():
        #     print(progress_data)
        # print("-- Magnetometer calibration finished")

        print("-- Starting board level horizon calibration")
        async for progress_data in pixhawkVehicle.calibration.calibrate_level_horizon():
            print(progress_data)
        print("-- Board level calibration finished")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


def checkIncomingLocation(droneDevice, incomingLocation):
    # Check the location and see if it is too close to the local drone
    # Incoming location: {'Lat': 47.3977418, 'Long': 8.545594099999999, 'rAlt': 0.0020000000949949026, 'aAlt': 488.010009765625}
    incomingLocationDict = json.loads(incomingLocation)
    localLocationDict = json.loads(getDroneCoordinates(droneDevice))

    localLocation = [
        localLocationDict["Lat"],
        localLocationDict["Lon"],
    ]
    incomingLocation = [
        incomingLocationDict["Lat"],
        incomingLocationDict["Lon"],
    ]

    map(float, localLocation)
    map(float, incomingLocation)

    distanceApart = geodesic(localLocation, incomingLocation).meters

    if distanceApart < droneDevice.getSafeDistance():
        print("Drone's GPS location close. Checking Altitude..")
        localAltitude = float(localLocationDict["aAlt"])
        incomingAltitude = float(incomingLocationDict["aAlt"])

        altitudeDistance = abs(localAltitude - incomingAltitude)

        if altitudeDistance < droneDevice.getSafeAltitude():
            print(f"TOO CLOSE, STOPPING {droneDevice.droneHumanName}")
            # TODO: This may be too slow of a way to stop the drone where it currently is.
            moveFromCurrent(droneDevice, (0, 0, 0))
        else:
            print("Altitude distance okay..")
    else:
        print("GPS location distance okay..")
        # TODO: Maybe we want to slow the drone down if the location is say 2x the safe distance


def default(droneDevice, additionalInfo=None):
    print("Incorrect syntax")
