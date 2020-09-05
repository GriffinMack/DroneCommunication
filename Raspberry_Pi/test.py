#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def run(drone):
    await drone.connect(system_address="udp://:14540")
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        absolute_latitude = terrain_info.latitude_deg
        absolute_longitude = terrain_info.longitude_deg
        break

    flying_alt = absolute_altitude + 20.0  # To fly drone 20m above the ground plane

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(absolute_latitude, absolute_longitude, flying_alt, 0)

    # wait for device to reach the desired altitude
    async for position in drone.telemetry.position():
        if position.absolute_altitude_m >= flying_alt:
            print("here")
            break
    
    await drone.action.goto_location(absolute_latitude, absolute_longitude + 1, flying_alt, 0)

    


    await asyncio.sleep(5)


async def openDrone():
    drone = System()
    print(type(drone))
    return drone

async def main():
    drone = await openDrone()
    await run(drone)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
