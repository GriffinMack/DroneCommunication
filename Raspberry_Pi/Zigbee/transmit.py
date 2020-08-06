# Brandon Stevens
# 12/3/2019
# Inital code pulled from https://jekhokie.github.io/raspberry-pi/raspbian/xbee/python/linux/electronics/2018/12/30/raspberry-pi-xbee-rxtx.html

#
# Transmits xbee messages over serial connection
#

# tranmission device id = 0x01
# receive device id = 0x00

# import libraries
import serial
import time
from xbee import XBee

# assign the XBee device settings and port numbers
SERIAL_PORT = "COM7"
BAUD_RATE = 9600

# configure the xbee
ser = serial.Serial(SERIAL_PORT, baudrate = BAUD_RATE)
xbee = XBee(ser, escaped = False)

# handler for sending data to a receiving XBee device
def send_data(data):
    xbee.send("tx", dest_addr=b'\x00\x01', data=bytes("{}".format(data), 'utf-8'))

# main loop/functionality
while True:
    try:
        print("Transmitting...")
        data = input("Enter data to send: ")
        send_data(data)

        time.sleep(0.3)
    except KeyboardInterrupt:
        break



#cleanup
ser.flushInput()
ser.flushOutput()
ser.close()
xbee.halt()
