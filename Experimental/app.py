# imports for front end functionality
import tkinter as tk
from tkinter import messagebox
import os

# imports for back end functionality
from Base_Station import networkDiscovery
window = tk.Tk()

window.title("Base Station")

window.geometry('700x700')

lbl = tk.Label(window, text="Hello")

lbl.grid(column=0, row=0)


def clicked():
    # discover the network
    discovered = networkDiscovery.discoverNetwork()
    messagebox.showinfo('2 Drones Discovered', 'Stanley\nCharlie')


btn = tk.Button(window, text="Discover XBEE Network", command=clicked)

btn.grid(column=1, row=0)

window.mainloop()
