# Brandon Stevens
# 12/8/2019

#
# Connects to PX4 firmware device and outputs some basic data
#

# Import DroneKit-Python
from dronekit import connect, Command, LocationGlobal
from pymavlink import mavutil
from xbee import XBee
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time, sys, argparse, math, mpu, serial

GPIO.setwarnings(False)    # Ignore warning for now
GPIO.setmode(GPIO.BOARD)   # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)   # Set pin 8 to be an output pin and set initial value to low (off)

# collision avoidance variables
mode = 0
safeDistance = 730 #feet
secondDroneLat = 33.214837 #degrees
secondDroneLong = -87.542813 #degrees

# assign the XBee device settings and ports
vehicle_connection_string = "/dev/ttyUSB1"
xbee_connection_string = "/dev/ttyUSB0"
BAUD_RATE = 9600

# handler for whenever data is received from transmitters - operates asynchronously
def receive_data(data):
    data = format(data['rf_data'])
    global mode
    mode = int(data)

# configure the xbee and enable asynchronous mode
ser = serial.Serial(xbee_connection_string, baudrate=BAUD_RATE)
xbee = XBee(ser, callback=receive_data, escaped=False)

# connect to the Vehicle
print ("Connecting...")

vehicle = connect(vehicle_connection_string, wait_ready=True) #vehicle is a px4 object

# display basic vehicle state
print (" Type: %s" % vehicle._vehicle_type)
print (" Armed: %s" % vehicle.armed)
print (" System status: %s" % vehicle.system_status.state)
print (" GPS: %s" % vehicle.gps_0)
print (" Alt: %s" % vehicle.location.global_relative_frame.alt)
print (" Heading: %s" % vehicle.heading)
print (" Mode: %s" % vehicle.mode.name)
isControlledOffBoard = input(" Connected!\nChoose (0) onboard or (1) offboard operating mode:")

while True:
    if isControlledOffBoard:
        print("Enter input from base station : ( 1 ) for general heading, ( 2 ) for distance to fountain, ( 3 ) for collision warning ")
        while mode == 0:
            #waiting for input from xbee device
            busyWork = 1
    else:
        mode = input("( 1 ) for general heading, ( 2 ) for distance to fountain, ( 3 ) for collision warning ")
    if mode == 1:
        count = 0
        while count < 250:
            print(" Heading: %s" % vehicle.heading)
            print(" %s" % vehicle.location.global_frame)
            print(" Velocity: %s" % vehicle.velocity)
            print(" GPS: %s\n" % vehicle.gps_0)
            time.sleep(0.1)
            count = count + 1

    elif mode == 2:
        # Drone location
        lat1 = vehicle.location.global_relative_frame.lat
        lon1 = vehicle.location.global_relative_frame.lon

        # Engineering Shelby quad fountain center
        lat2 = 33.214837
        lon2 = -87.542813

        # Distance calculation
        dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2)) #km
        dist = dist * 3280.24 #km -> feet
        print("Feet to Shelby Engineering Quad Fountain : ", dist)

    elif mode == 3:
        
        count = 0
        while count < 50:
            # Drone location
            lat1 = vehicle.location.global_relative_frame.lat
            lon1 = vehicle.location.global_relative_frame.lon

            # second drone location
            lat2 = secondDroneLat
            lon2 = secondDroneLong

            # Distance calculation
            dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2)) #km
            dist = dist * 3280.24 #km -> feet
            print(dist, " feet")
            if dist < safeDistance:
                GPIO.output(8, GPIO.HIGH) # Turn on
                print("Unsafe distance!")
            else:
                GPIO.output(8, GPIO.LOW) # Turn off
            time.sleep(0.5)
            count = count + 1

    else:
        print("Invalid input")
    mode = 0

print("Done!")
sys.exit()
