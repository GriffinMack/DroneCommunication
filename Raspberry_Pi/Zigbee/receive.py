# Brandon Stevens
# 12/3/2019
# Inital code pulled from https://jekhokie.github.io/raspberry-pi/raspbian/xbee/python/linux/electronics/2018/12/30/raspberry-pi-xbee-rxtx.html

#
# Receives xbee messages over serial connection
#

# tranmission device id = 0x01
# receive device id = 0x00

# import libraries
import serial
import time
from xbee import XBee

# assign the XBee device settings and port numbers
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# handler for whenever data is received from transmitters - operates asynchronously
def receive_data(data):
    print("Received data packet: {}".format(data))
    rx = data['rf_data'].decode('utf-8')

    print("Data: {}".format(data['rf_data']))

# configure the xbee and enable asynchronous mode
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE)
xbee = XBee(ser, callback=receive_data, escaped=False)


# main loop/functionality
while True:
    try:
        # operate in async mode where all messages will go to handler
        time.sleep(0.001)
    except KeyboardInterrupt:
        break

#cleanup
ser.flushInput()
ser.flushOutput()
ser.close()
xbee.halt()
