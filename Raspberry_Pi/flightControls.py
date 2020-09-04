# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time


def decodeMessage(droneDevice, incomingMessage):
    # takes the incoming message and finds a flight control that corresponds
    flightControls = {"takeoff": takeoffDrone,
                      "land": landDrone,
                      "move to coordinate: ": moveToCoordinates,
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
                      "right": manuallyMoveDroneRight
                      }
    return flightControls[incomingMessage](droneDevice.pixhawkDevice)


def getDroneCoordinates(pixhawkDevice):

    # TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call

    print(f"Global Location: {pixhawkDevice.pixhawkVehicle.location.global_frame}")
    print(
        f"Global Location (relative altitude): {pixhawkDevice.pixhawkVehicle.location.global_relative_frame}")
    print(f"Local Location: {pixhawkDevice.pixhawkVehicle.location.local_frame}")  # NED
    print(f"Attitude: {pixhawkDevice.pixhawkVehicle.attitude}")
    print(f"Velocity: {pixhawkDevice.pixhawkVehicle.velocity}")
    print(f"GPS: {pixhawkDevice.pixhawkVehicle.gps_0}")
    print(f"Groundspeed: {pixhawkDevice.pixhawkVehicle.groundspeed}")
    print(f"Airspeed: {pixhawkDevice.pixhawkVehicle.airspeed}")

    # TODO: Take the most helpful items and send them back to the base station through the Zigbee (find an efficient way to do this. We don't want to send 20 different messages just for basic info. Maybe combine everything into one string and break it back up on the other end)


def getDroneSummary(pixhawkDevice):

    # TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call
    print(f"Autopilot Firmware version: {pixhawkDevice.pixhawkVehicle.version}")
    print(f"Autopilot capabilities (supports ftp): {pixhawkDevice.pixhawkVehicle.capabilities.ftp}")
    print(f"Global Location: {pixhawkDevice.pixhawkVehicle.location.global_frame}")
    print(
        f"Global Location (relative altitude): {pixhawkDevice.pixhawkVehicle.location.global_relative_frame}")
    print(f"Local Location: {pixhawkDevice.pixhawkVehicle.location.local_frame}")  # NED
    print(f"Attitude: {pixhawkDevice.pixhawkVehicle.attitude}")
    print(f"Velocity: {pixhawkDevice.pixhawkVehicle.velocity}")
    print(f"GPS: {pixhawkDevice.pixhawkVehicle.gps_0}")
    print(f"Groundspeed: {pixhawkDevice.pixhawkVehicle.groundspeed}")
    print(f"Airspeed: {pixhawkDevice.pixhawkVehicle.airspeed}")
    print(f"Gimbal status: {pixhawkDevice.pixhawkVehicle.gimbal}")
    print(f"Battery: {pixhawkDevice.pixhawkVehicle.battery}")
    print(f"EKF OK?: {pixhawkDevice.pixhawkVehicle.ekf_ok}")
    print(f"Last Heartbeat: {pixhawkDevice.pixhawkVehicle.last_heartbeat}")
    print(f"Rangefinder: {pixhawkDevice.pixhawkVehicle.rangefinder}")
    print(f"Rangefinder distance: {pixhawkDevice.pixhawkVehicle.rangefinder.distance}")
    print(f"Rangefinder voltage: {pixhawkDevice.pixhawkVehicle.rangefinder.voltage}")
    print(f"Heading: {pixhawkDevice.pixhawkVehicle.heading}")
    print(f"Is Armable?: {pixhawkDevice.pixhawkVehicle.is_armable}")
    print(f"System status: {pixhawkDevice.pixhawkVehicle.system_status.state}")
    print(f"Groundspeed: {pixhawkDevice.pixhawkVehicle.groundspeed}")    # settable
    print(f"Airspeed: {pixhawkDevice.pixhawkVehicle.airspeed}")    # settable
    print(f"Mode: {pixhawkDevice.pixhawkVehicle.mode.name}")  # settable
    print(f"Armed: {pixhawkDevice.pixhawkVehicle.armed}")    # settable

    # TODO: Take the most helpful items and send them back to the base station through the Zigbee (find an efficient way to do this. We don't want to send 20 different messages just for basic info. Maybe combine everything into one string and break it back up on the other end)


def takeoffDrone(pixhawkDevice):

    # TODO: Grab the target hover altitude (should be sent to the Zigbee from the base station)
    targetAltitude = 20

    def arm_and_takeoff(pixhawkDevice, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """
        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        # This attribute wraps a number of pre-arm checks, ensuring that the vehicle has booted, has a good GPS fix, and that the EKF pre-arm is complete.
        while not pixhawkDevice.pixhawkVehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        # Copter should arm in GUIDED mode
        pixhawkDevice.pixhawkVehicle.mode = VehicleMode("GUIDED")
        pixhawkDevice.pixhawkVehicle.armed = True

        # Confirm vehicle armed before attempting to take off
        while not pixhawkDevice.pixhawkVehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        pixhawkDevice.pixhawkVehicle.simple_takeoff(
            aTargetAltitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto
        #  (otherwise the command after Vehicle.simple_takeoff will execute
        #   immediately).
        while True:
            print(
                " Altitude: ", pixhawkDevice.pixhawkVehicle.location.global_relative_frame.alt)
            # Break and return from function just below target altitude.
            if pixhawkDevice.pixhawkVehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)
    arm_and_takeoff(pixhawkDevice, targetAltitude)


def landDrone(pixhawkDevice):

    # TODO: Grab the target landing coordinates (should be sent to the Zigbee from the base station. Should default to the current RTL location if no landing location is specified by the user)
    targetAltitude = "..."
    targetLongitude = "..."
    targetLatitude = "..."

    # Get Vehicle Home location - will be `None` until first set by autopilot
    while not pixhawkDevice.pixhawkVehicle.home_location:
        cmds = pixhawkDevice.pixhawkVehicle.commands
        cmds.download()
        cmds.wait_ready()
        if not pixhawkDevice.pixhawkVehicle.home_location:
            print(" Waiting for home location ...")

    # We have a home location.
    print(f"\n Home location: {pixhawkDevice.pixhawkVehicle.home_location}")

    # TODO: Set the home location if wanting to land somewhere different than the takeoff location (perhaps give the user the option to RTL, land in the current location, or give landing coordinates)
    pixhawkDevice.pixhawkVehicle.home_location = pixhawkDevice.pixhawkVehicle.location.global_frame(
        targetLatitude, targetLongitude, targetAltitude)

    # Land at the launch location (The Home location is set when a vehicle first gets a good location fix from the GPS. The location is used as the target when the vehicle does a “return to launch”.)
    print("Returning to Launch")
    pixhawkDevice.pixhawkVehicle.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print("Close vehicle object")
    pixhawkDevice.pixhawkVehicle.close()


def moveToCoordinates(pixhawkDevice):

    # TODO: Grab the target location (should be sent to the Zigbee from the base station)
    targetAltitude = "..."
    targetLongitude = "..."
    targetLatitude = "..."

    print("Set default/target airspeed to 3")
    pixhawkDevice.pixhawkVehicle.airspeed = 3
    # TODO: Allow configuration of the airspeed

    print("Going towards first point for 30 seconds ...")
    # TODO:
    # LocationGlobalRelative goes 'targetAltitude' meters in altitude relative from the home point
    point1 = LocationGlobalRelative(
        targetLatitude, targetLongitude, targetAltitude)
    pixhawkDevice.pixhawkVehicle.simple_goto(point1)

    # sleep so we can see the change in position
    time.sleep(30)


def homeLocationHover(pixhawkDevice):
    pass


def followBaseStation(pixhawkDevice):
    pass


def manuallyMoveDroneUp(pixhawkDevice):
    print("moving drone up")


def manuallyRotateDroneLeft(droneDevice):
    print("moving drone left")


def manuallyRotateDroneRight(droneDevice):
    print("moving drone right")


def manuallyMoveDroneDown(droneDevice):
    print("moving drone down")


def manuallyMoveDroneForward(droneDevice):
    print("moving drone forward")


def manuallyMoveDroneBackward(droneDevice):
    print("moving drone backward")


def manuallyMoveDroneLeft(droneDevice):
    print("moving drone left")


def manuallyMoveDroneRight(droneDevice):
    print("moving drone right")
