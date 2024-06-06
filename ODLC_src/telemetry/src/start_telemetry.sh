#!/bin/bash

# Start the heartbeat script
python ./heartbeat.py &

# Start the receiver script
python ./Receiver.py &

# Start the requester script
python ./Requester.py &

# Start the sender script
python ./Sender.py &

# Wait for all background processes to finish
wait
