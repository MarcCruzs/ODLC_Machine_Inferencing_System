#!/bin/bash

while true; do
  # Wait for camera to complete
  while [ ! -f /usr/app/status/camera.done ]; do
    echo "Waiting for camera to complete..."
    sleep 0.1
  done

  # Shape human tasks
  echo "Running shape human tasks..."

  #get an image from volume 1
  image_file=$(find /raw_images -maxdepth 1 -type f -name "*.jpg" -print -quit)

  if [ -z "$image_file" ]; then
      echo "no image found in volume"
      exit 1
  fi

  #run HUMAN detection script
  python ./src/detect.py --source /raw_images/$(basename "$image_file") --weights ./src/HumanModel.pt --save-txt --name HumanModelResults

  #run Shape detection script
  python ./src/detect.py --source /raw_images/$(basename "$image_file") --weights ./src/ShapeModel.pt --save-txt --name ShapeModelResults

  #copy image to volume 2 and remove it from first volume
  cp "$image_file" /imagebank

  rm /raw_images/$(basename "$image_file")

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