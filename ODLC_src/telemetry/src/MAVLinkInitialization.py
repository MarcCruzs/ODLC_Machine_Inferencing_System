import asyncio
from pymavlink import mavutil
import os
import MAVLinkInitialization  # Import the heartbeat module

async def handle_camera_trigger_distance(distance):
    """
    Handle the camera trigger distance command by invoking the camera service.

    Parameters:
    - distance: The distance between camera triggers in meters.
    """
    print(f"Received camera trigger distance command: {distance} meters")

    # Trigger the camera service by creating a trigger file
    trigger_file = "/usr/app/status/camera_trigger"
    if not os.path.exists("/usr/app/status"):
        os.makedirs("/usr/app/status")
    
    with open(trigger_file, 'w') as f:
        f.write('trigger')
    print("Camera trigger file created.")

async def receive_commands():
    """
    Receive MAVLink commands and handle them accordingly.
    """
    master = MAVLinkInitialization.master
    while True:
        msg = master.recv_match(blocking=True)
        if not msg:
            continue
        
        if msg.get_type() == "COMMAND_LONG" and msg.command == mavutil.mavlink.MAV_CMD_DO_SET_CAM_TRIGG_DIST:
            distance = msg.param1
            await handle_camera_trigger_distance(distance)
        else:
            print("Received message: %s" % msg)
        await asyncio.sleep(0.1)  # Short sleep to yield control to other tasks

async def main():
    # Ensure heartbeat is established
    while MAVLinkInitialization.master is None:
        print("Waiting for MAVLink connection to be established by heartbeat.py...")
        await asyncio.sleep(1)

    await receive_commands()

if __name__ == "__main__":
    asyncio.run(main())
