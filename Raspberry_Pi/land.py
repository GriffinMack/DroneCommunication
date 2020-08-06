#
# Connects to PX4 firmware device and initiates a drone landing.
#
#
# Print statements are for debugging purposes only (prints display on Raspberry Pi)
#

# Import DroneKit-Python
from dronekit import connect, VehicleMode
import time

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
        print " Waiting for home location ..."

# We have a home location.
print "\n Home location: %s" % vehicle.home_location

# TODO: Set the home location if wanting to land somewhere different than the takeoff location (perhaps give the user the option to RTL, land in the current location, or give landing coordinates)
vehicle.home_location = vehicle.location.global_frame(targetLatitude, targetLongitude, targetAltitude)

# Land at the launch location (The Home location is set when a vehicle first gets a good location fix from the GPS. The location is used as the target when the vehicle does a “return to launch”.)
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
