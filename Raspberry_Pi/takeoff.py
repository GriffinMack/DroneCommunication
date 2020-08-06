#
# Connects to PX4 firmware device and initiates a drone take-off.
#
#
# Print statements are for debugging purposes only (prints display on Raspberry Pi)
#

# Import DroneKit-Python
from dronekit import connect, VehicleMode
import time

# specify port the vehicle is connected to
vehicle_connection_string = "/dev/ttyUSB1"

# TODO: Grab the target hover altitude (should be sent to the Zigbee from the base station)
targetAltitude = "..."

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