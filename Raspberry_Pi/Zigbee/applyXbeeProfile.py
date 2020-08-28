from digi.xbee.devices import XBeeDevice

def applyProfile():
    # TODO: Replace with the location of the XBee profile file to read.
    PROFILE_PATH = "<path_to_profile>"
    # TODO: Replace with the serial port where your local module is connected to.
    PORT = "COM1"
    # TODO: Replace with the baud rate of your local module.
    BAUD_RATE = 9600
    print(" +------------------------------------------------+")
    print(" | APPLYING CURRENT XBEE PROFILE FOR BASE STATION |")
    print(" +------------------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    try:
        device.open()
        print("Updating profile '%s'...\n" % PROFILE_PATH)
        device.apply_profile(PROFILE_PATH, progress_callback=progress_callback)
        print("\nProfile updated successfully!")
    except Exception as e:
        print(str(e))
        exit(1)
    finally:
        if device.is_open():
            device.close()


def progress_callback(task, percent):
    if percent is not None:
        print("%s: %d%%" % (task, percent))
    else:
        print("%s" % task)