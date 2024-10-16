#!/bin/sh

while true; do
  # Wait for telemetry to complete
  while [ ! -f /usr/app/status/telemetry.done ]; do
    echo "Waiting for telemetry to complete..."
    sleep 0.1
  done

  # Camera tasks
  echo "Running camera tasks..."
  python camera.py --folder1 /usr/app/src/folder1/ --folder2 /usr/app/src/folder2/

  # Signal completion
  touch /usr/app/status/camera.done

  echo "Camera tasks completed. Waiting for reset..."

  # Wait for reset signal
  while [ ! -f /usr/app/status/reset.done ]; do
    sleep 1
  done

  # Reset status
  rm /usr/app/status/camera.done /usr/app/status/reset.done
done
