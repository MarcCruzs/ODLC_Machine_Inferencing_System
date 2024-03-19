from pymavlink import mavutil

# Callback function to handle incoming GPS messages
def handle_gps_message(message):
    if message.get_type() == 'GLOBAL_POSITION_INT':
        altitude = message.alt / 1e3  # Convert from millimeters to meters
        print(f"Altitude: {altitude} meters")

def main():
    # Connect to the UAV (Pixhawk)
    master = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

    # Wait for the heartbeat message to ensure UAV connection
    master.wait_heartbeat()

    # Subscribe to GPS messages
    master.mav.request_data_stream_send(
        master.target_system,   # Target system
        master.target_component,  # Target component
        mavutil.mavlink.MAV_DATA_STREAM_POSITION,  # Request position data stream
        1,  # Enable
        1   # Rate (Hz)
    )

    # Main loop to continuously handle incoming messages
    while True:
        try:
            message = master.recv_match(type=['GLOBAL_POSITION_INT'], timeout=1)
            if message is not None:
                handle_gps_message(message)
        except KeyboardInterrupt:
            break

    # Close the connection
    master.close()

if __name__ == "__main__":
    main()
