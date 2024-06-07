#!/bin/sh

while true; do
  # Wait for alphanumeric to complete
  while [ ! -f /usr/app/status/alphanumeric.done ]; do
    echo "Waiting for alphanumeric to complete..."
    sleep 0.1
    # Removed sleep for faster checking
    :
  done

  # Checklist and location tasks
  echo "Running checklist and location tasks..."
  # (Add your checklist and location tasks here)

  # Signal completion
  touch /usr/app/status/checklist_and_location.done

  echo "Checklist and location tasks completed. Triggering reset..."

  # Trigger reset signal
  touch /usr/app/status/reset.done

  # Wait for a short period to ensure all services have reset
  sleep 1

  # Reset status files
  rm /usr/app/status/checklist_and_location.done /usr/app/status/alphanumeric.done /usr/app/status/color.done /usr/app/status/shape_human.done /usr/app/status/camera.done /usr/app/status/telemetry.done /usr/app/status/reset.done
done
