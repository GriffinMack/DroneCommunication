# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time, json


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
    flightControls[incomingMessage](droneDevice)


def getDroneCoordinates():
    # specify port the vehicle is connected to
    vehicle_connection_string = "/dev/ttyUSB1"

    # connect to the Vehicle
    print("Connecting...")
    vehicle = connect(vehicle_connection_string, wait_ready=True, baud=57600)

    # TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call
    # Create dictionary of drone coordinates info
    droneCoordinates = {
        "Global Location": vehicle.location.global_frame,
        "Global Location (relative altitude)": vehicle.location.global_relative_frame,
        "Local Location": vehicle.location.local_frame,
        "Attitude": vehicle.attitude,
        "Velocity": vehicle.velocity,
        "GPS": vehicle.gps_0,
        "Groundspeed": vehicle.groundspeed,
        "Airspeed": vehicle.airspeed
    }

    # Convert into json string
    jsDroneCoordinates = json.dumps(droneCoordinates)

    # Take the most helpful items and send them back to the base station through the Zigbee 
    return jsDroneCoordinates


def getDroneSummary():
    # specify port the vehicle is connected to
    vehicle_connection_string = "/dev/ttyUSB1"

    # connect to the Vehicle
    print("Connecting...")
    vehicle = connect(vehicle_connection_string, wait_ready=True, baud=57600)

    # TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call
    # Create python dictionary of Drone Summary Info
    droneSummary = {
        "Autopilot Firmware version": vehicle.version,
        "Autopilot capabilities (supports ftp)": vehicle.capabilities.ftp,
        "Global Location": vehicle.location.global_frame,
        "Global Location (relative altitude)": vehicle.location.global_relative_frame,
        "Local Location": vehicle.location.local_frame,
        "Attitude": vehicle.attitude,
        "Velocity": vehicle.velocity,
        "GPS": vehicle.gps_0,
        "Groundspeed": vehicle.groundspeed,
        "Airspeed": vehicle.airspeed,
        "Gimbal status": vehicle.gimbal,
        "Battery": vehicle.battery,
        "EKF OK?": vehicle.ekf_ok,
        "Last Heartbeat": vehicle.last_heartbeat,
        "Rangefinder": vehicle.rangefinder,
        "Rangefinder distance": vehicle.rangefinder.distance,
        "Rangefinder voltage": vehicle.rangefinder.voltage,
        "Heading": vehicle.heading,
        "Is Armable?": vehicle.is_armable,
        "System status": vehicle.system_status.state,
        "Groundspeed": vehicle.groundspeed,     # settable
        "Airspeed": vehicle.airspeed,           # settable
        "Mode": vehicle.mode.name,              # settable
        "Armed": vehicle.armed                  # settable
    }

    # Convert Drone Summary info into json string
    jsDroneSummary = json.dumps(droneSummary)

    # Take the most helpful items and send them back to the base station through the Zigbee 
    return jsDroneSummary


def takeoffDrone():
    # specify port the vehicle is connected to
    vehicle_connection_string = "/dev/ttyUSB1"

    # Grab the target hover altitude (should be sent to the Zigbee from the base station)
    droneDevice.sendMessage("Please enter target hover altitude: ")
    message = droneDevice.pollForIncomingMessage()
    targetAltitude = decodeMessage(droneDevice, message)
    print("Target altitude: ", targetAltitude)

    # connect to the Vehicle
    print("Connecting...")
    vehicle = connect(vehicle_connection_string, wait_ready=True, baud=57600)

    def arm_and_takeoff(aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        # This attribute wraps a number of pre-arm checks, ensuring that the vehicle has booted, has a good GPS fix, and that the EKF pre-arm is complete.
        while not vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        # Copter should arm in GUIDED mode
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True

        # Confirm vehicle armed before attempting to take off
        while not vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto
        #  (otherwise the command after Vehicle.simple_takeoff will execute
        #   immediately).
        while True:
            print(" Altitude: ", vehicle.location.global_relative_frame.alt)
            # Break and return from function just below target altitude.
            if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)
    arm_and_takeoff(targetAltitude)


def landDrone():
    # specify port the vehicle is connected to
    vehicle_connection_string = "/dev/ttyUSB1"

    # connect to the Vehicle
    print("Connecting...")
    vehicle = connect(vehicle_connection_string, wait_ready=True, baud=57600)

    # TODO: Grab the target landing coordinates (should be sent to the Zigbee from the base station. Should default to the current RTL location if no landing location is specified by the user)
    targetAltitude = "..."
    targetLongitude = "..."
    targetLatitude = "..."

    # Get Vehicle Home location - will be `None` until first set by autopilot
    while not vehicle.home_location:
        cmds = vehicle.commands
        cmds.download()
        cmds.wait_ready()
        if not vehicle.home_location:
            print(" Waiting for home location ...")

    # We have a home location.
    print(f"\n Home location: {vehicle.home_location}")

    # TODO: Set the home location if wanting to land somewhere different than the takeoff location (perhaps give the user the option to RTL, land in the current location, or give landing coordinates)
    vehicle.home_location = vehicle.location.global_frame(
        targetLatitude, targetLongitude, targetAltitude)

    # Land at the launch location (The Home location is set when a vehicle first gets a good location fix from the GPS. The location is used as the target when the vehicle does a “return to launch”.)
    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()


def moveToCoordinates(coordinates):
    # specify port the vehicle is connected to
    vehicle_connection_string = "/dev/ttyUSB1"

    # TODO: Grab the target location (should be sent to the Zigbee from the base station)
    targetAltitude = "..."
    targetLongitude = "..."
    targetLatitude = "..."

    # TODO: Do we need to connect again? connect to the Vehicle
    print("Connecting...")
    vehicle = connect(vehicle_connection_string, wait_ready=True, baud=57600)

    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3
    # TODO: Allow configuration of the airspeed

    print("Going towards first point for 30 seconds ...")
    # TODO:
    # LocationGlobalRelative goes 'targetAltitude' meters in altitude relative from the home point
    point1 = LocationGlobalRelative(
        targetLatitude, targetLongitude, targetAltitude)
    vehicle.simple_goto(point1)

    # sleep so we can see the change in position
    time.sleep(30)


def homeLocationHover():
    pass


def followBaseStation():
    pass


def manuallyMoveDroneUp(droneDevice):
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

