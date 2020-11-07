  
#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def run():
    drone = System(mavsdk_server_address="localhost")
    await drone.connect(system_address="serial:///dev/ttyUSB0")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    info = await drone.info.get_version()
    print(info)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())