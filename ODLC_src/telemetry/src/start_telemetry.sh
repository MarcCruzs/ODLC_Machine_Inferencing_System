#!/bin/sh

# Start the heartbeat script
python /usr/app/heartbeat.py &

# Start the receiver script
python /usr/app/Receiver.py &

# Start the requester script
python /usr/app/Requester.py &

# Start the sender script
python /usr/app/Sender.py &

# Wait for all background processes to finish
wait
