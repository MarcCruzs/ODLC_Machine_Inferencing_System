import asyncio
from pymavlink import mavutil
import MAVLinkInitialization  # Import the heartbeat module
from flask import Flask, jsonify

app = Flask(__name__)

async def request_gps_data():
    master = MAVLinkInitialization.master
    master.mav.request_data_stream_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_POSITION, 1, 1
    )
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    if msg:
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1e3
        return {"latitude": lat, "longitude": lon, "altitude": alt}
    return {"error": "No GPS data received"}

@app.route('/gps', methods=['GET'])
def get_gps_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    gps_data = loop.run_until_complete(request_gps_data())
    return jsonify(gps_data)

async def main():
    # Ensure heartbeat is established
    while MAVLinkInitialization.master is None:
        print("Waiting for MAVLink connection to be established by heartbeat.py...")
        await asyncio.sleep(1)

    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    asyncio.run(main())
