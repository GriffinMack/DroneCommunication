from mavsdk import System
import asyncio
import time

"""
A class used to represent a pixhawk.
...

Attributes
----------
Methods
-------
"""


class PixhawkDevice:
    def __init__(self):
        self.pixhawkVehicle = self.connectToVehicle()

    def connectToVehicle(self):
        async def simulator(self):
            async def openSimulation():
                return System()

            async def openDrone():
                return System(mavsdk_server_address="localhost")

            async def connectToSimulator(drone):
                await drone.connect(system_address="udp://:14540")
                print("Waiting for drone to connect...")
                async for state in drone.core.connection_state():
                    if state.is_connected:
                        print(f"Drone discovered with UUID: {state.uuid}")
                        self.pixhawkVehicle = drone
                        break

            async def connectToDrone(drone):
                # TODO: Connect to the correct USB device connected to the Pixhawk
                await drone.connect(system_address="USB DEVICE....")
                print("Waiting for drone to connect...")
                async for state in drone.core.connection_state():
                    if state.is_connected:
                        print(f"Drone discovered with UUID: {state.uuid}")
                        self.pixhawkVehicle = drone
                        break

            drone = await openSimulation()
            await connectToSimulator(drone)

        # Start SITL if no pixhawk device is found
        loop = asyncio.get_event_loop()
        loop.run_until_complete(simulator(self))
        return self.pixhawkVehicle

    def getPixhawkVehicle(self):
        return self.pixhawkVehicle