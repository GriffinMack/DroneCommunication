# Griffin Mack
# 8/30/2020
#
# Tkinter program that captures keyboard input from WASD and arrow keys to control the movement of a drone. Assumes the messages sent are being parsed correctly by the Raspberry Pi.
#
# NOTE: If the droneToControl remains blank, ALL drones (if they receive) will move together.

# Python3
import tkinter as tk


def controlDronesManually(baseStationXbee, droneToControl=None):
    def key(event):
        """shows key or tk code for the key"""
        if event.keysym == 'Escape':
            root.destroy()
        if event.char == event.keysym:
            # normal number and letter characters (WASD)
            print('Normal Key %r' % event.char)
            if(event.char == "w"):
                baseStationXbee.sendMessage("up", droneToControl)
            elif(event.char == "a"):
                baseStationXbee.sendMessage("left rotate", droneToControl)

            elif(event.char == "s"):
                baseStationXbee.sendMessage("down", droneToControl)

            elif(event.char == "d"):
                baseStationXbee.sendMessage("right rotate", droneToControl)

        elif len(event.char) == 1:
            # arrow keys
            print(f'Punctuation Key {event.keysym}')
            if(event.keysym == "Up"):
                baseStationXbee.sendMessage("forward", droneToControl)
            elif(event.keysym == "Left"):
                baseStationXbee.sendMessage("left", droneToControl)
            elif(event.keysym == "Down"):
                baseStationXbee.sendMessage("backward", droneToControl)
            elif(event.keysym == "Right"):
                baseStationXbee.sendMessage("right", droneToControl)

    root = tk.Tk()
    print("Press a key (Escape key to exit):")
    root.bind_all('<Key>', key)

    # don't show the tk window
    # root.withdraw()
    root.mainloop()
