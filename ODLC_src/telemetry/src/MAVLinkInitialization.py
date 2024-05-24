from pymavlink import mavutil

def main():
    port = 'COM7'

    try:
        master = mavutil.mavlink_connection(port)
        print("MAVLink connection established")

        while True:
            msg = master.recv_match(type='HEARTBEAT', blocking=True)
            if msg:
                print("Received Heartbeat: %s" % msg)

    except mavutil.MavError as e:
        print(f"MAVLink error: {e}")

    except Exception as e:
         print(f"Error: {e}")

if __name__ == "__main__":
    main()