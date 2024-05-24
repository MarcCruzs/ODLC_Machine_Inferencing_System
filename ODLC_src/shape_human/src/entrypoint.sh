#!/bin/bash

while true; do
  # Wait for camera to complete
  while [ ! -f /usr/app/status/camera.done ]; do
    echo "Waiting for camera to complete..."
    sleep 0.1
  done

  # Shape human tasks
  echo "Running shape human tasks..."

  # Get an image from volume 1
  image_file=$(find /usr/app/raw_images -maxdepth 1 -type f -name "*.jpg" -print -quit)

  if [ -z "$image_file" ]; then
      echo "No image found in volume"
      exit 1
  fi

  # Run HUMAN detection script
  echo "Running human detection script..."
  python ./src/detect.py --source "$image_file" --weights ./src/HumanModel.pt --save-txt --name HumanModelResults

  # Run Shape detection script
  echo "Running shape detection script..."
  python ./src/detect_objects.py --source "$image_file" --conf_threshold 0.60 --save_dir /usr/app/cropped_images --checklist_path /usr/app/checklist/output.txt

  # Copy image to volume 2 and remove it from first volume
  echo "Copying image to volume 2 and removing it from volume 1..."
  cp "$image_file" /usr/app/imagebank
  rm "$image_file"

  # Signal completion
  touch /usr/app/status/shape_human.done

  echo "Shape human tasks completed. Waiting for reset..."

  # Wait for reset signal
  while [ ! -f /usr/app/status/reset.done ]; do
    sleep 0.5
  done

  # Reset status
  rm /usr/app/status/shape_human.done /usr/app/status/reset.done
done
