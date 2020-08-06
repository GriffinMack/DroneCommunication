#
# Connects to PX4 firmware device and moves to inputted coordinates.
#
# ASSUMPTIONS: Vehicle has already taken off and is hovering
#
# Print statements are for debugging purposes only (prints display on Raspberry Pi)
#

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

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
#LocationGlobalRelative goes 'targetAltitude' meters in altitude relative from the home point
point1 = LocationGlobalRelative(targetLatitude, targetLongitude, targetAltitude)
vehicle.simple_goto(point1)

# sleep so we can see the change in position
time.sleep(30)