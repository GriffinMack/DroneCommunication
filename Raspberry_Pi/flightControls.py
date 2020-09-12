import time
import asyncio


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
        "manual control": manualControl,
    }
    # Check for any additional info in the command (should be split by a :)
    try:
        incomingMessage, additionalInfo = incomingMessage.split(":")
    except:
        additionalInfo = None
    return flightControls[incomingMessage](droneDevice, additionalInfo)


def getDroneCoordinates(droneDevice, additionalInfo=None):
    pass
    # TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call

    # TODO: Take the most helpful items and send them back to the base station through the Zigbee (find an efficient way to do this. We don't want to send 20 different messages just for basic info. Maybe combine everything into one string and break it back up on the other end)


def getDroneSummary(droneDevice, additionalInfo=None):
    pass
    # TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call

    # TODO: Take the most helpful items and send them back to the base station through the Zigbee (find an efficient way to do this. We don't want to send 20 different messages just for basic info. Maybe combine everything into one string and break it back up on the other end)


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

        # TODO: Get the user inputted coordinates from the XBEE message
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

        # TODO: Check if the drone is actually in the air

        await asyncio.sleep(1)
        flying_alt = absolute_altitude + 20.0  # To fly drone 20m above the ground plane

        # goto_location() takes Absolute MSL altitude
        await pixhawkVehicle.action.goto_location(
            latitude + 0.0002, longitude + 0.0002, flying_alt, 0
        )

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
        flying_alt = absolute_altitude + 10.0  # To hover drone 10m above ground

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

        manualControls = {
            "up": [0,0,1,0], #throttle max
            "down": [0,0,0,0], #throttle min
            "left": [0,0,0.5,-1], #yaw min
            "right": [0,0,0.5,1], #yaw max
            "left rotate": [0,-1,0.5,0], #pitch min
            "right rotate": [0,1,0.5,0], #pitch max
            "forward": [1,0,0.5,0], #roll max
            "backward": [-1,0,0.5,0], #roll min
        }
        while True:
            # check for a xbee message
            # TODO: Check is taking up too much time
            message = xbeeDevice.pollForIncomingMessage()

            manualControlsInput = [0,0,0.5,0]
            if message in manualControls:
                manualControlsInput = manualControls[message]
            map(float, manualControlsInput)

            print(manualControlsInput)
            await pixhawkVehicle.manual_control.set_manual_control_input(
                *manualControlsInput
            )

            await asyncio.sleep(0.1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(manual_controls())