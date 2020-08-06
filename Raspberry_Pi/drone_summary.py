#
# Connects to PX4 firmware device and reads some basic data
#
# Written to be ran on the onboard raspberry Pi. HOWEVER, this should work by plugging PX4 into a laptop usb port (may # require editing the vehicle_connection_string)
#
# Print statements are for debugging purposes only (prints display on Raspberry Pi)
#

# Import DroneKit-Python
from dronekit import connect

# specify port the vehicle is connected to
vehicle_connection_string = "/dev/ttyUSB1"

# connect to the Vehicle
print("Connecting...")
vehicle = connect(vehicle_connection_string, wait_ready=True, baud=57600)

# TODO: Go through these items and find ones that are actually helpful. Maybe leave all non-helpful items in and allow an optional "verbose" call
print(f"Autopilot Firmware version: {vehicle.version}")
print(f"Autopilot capabilities (supports ftp): {vehicle.capabilities.ftp}")
print(f"Global Location: {vehicle.location.global_frame}")
print(f"Global Location (relative altitude): {vehicle.location.global_relative_frame}")
print(f"Local Location: {vehicle.location.local_frame}")  # NED
print(f"Attitude: {vehicle.attitude}")
print(f"Velocity: {vehicle.velocity}")
print(f"GPS: {vehicle.gps_0}")
print(f"Groundspeed: {vehicle.groundspeed}")
print(f"Airspeed: {vehicle.airspeed}")
print(f"Gimbal status: {vehicle.gimbal}")
print(f"Battery: {vehicle.battery}")
print(f"EKF OK?: {vehicle.ekf_ok}")
print(f"Last Heartbeat: {vehicle.last_heartbeat}")
print(f"Rangefinder: {vehicle.rangefinder}")
print(f"Rangefinder distance: {vehicle.rangefinder.distance}")
print(f"Rangefinder voltage: {vehicle.rangefinder.voltage}")
print(f"Heading: {vehicle.heading}")
print(f"Is Armable?: {vehicle.is_armable}")
print(f"System status: {vehicle.system_status.state}")
print(f"Groundspeed: {vehicle.groundspeed}")    # settable
print(f"Airspeed: {vehicle.airspeed}")    # settable
print(f"Mode: {vehicle.mode.name}")  # settable
print(f"Armed: {vehicle.armed}")    # settable

# TODO: Take the most helpful items and send them back to the base station through the Zigbee (find an efficient way to do this. We don't want to send 20 different messages just for basic info. Maybe combine everything into one string and break it back up on the other end)