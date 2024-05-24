import asyncio
from pymavlink import mavutil
import MAVLinkInitialization  # Import the heartbeat module

async def send_waypoints():
    master = MAVLinkInitialization.master
    waypoints = [
        (47.397742, 8.545594, 10),  # (latitude, longitude, altitude)
        (47.397750, 8.545600, 15)
    ]
    
    for i, wp in enumerate(waypoints):
        lat, lon, alt = wp
        msg = master.mav.mission_item_int_encode(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,
            int(lat*1e7), int(lon*1e7), alt, i
        )
        master.mav.send(msg)
        print(f"Sent waypoint {i+1}: Latitude={lat}, Longitude={lon}, Altitude={alt} meters")
        await asyncio.sleep(1)

async def main():
    # Ensure heartbeat is established
    while MAVLinkInitialization.master is None:
        print("Waiting for MAVLink connection to be established by heartbeat.py...")
        await asyncio.sleep(1)

    await send_waypoints()

if __name__ == "__main__":
    asyncio.run(main())
