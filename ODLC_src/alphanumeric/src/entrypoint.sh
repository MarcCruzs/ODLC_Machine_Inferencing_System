#!/bin/bash

while true; do
  # Wait for color to complete
  while [ ! -f /usr/app/status/color.done ]; do
    echo "Waiting for color to complete..."
    sleep 0.1
  done

  #get an image from volume 1
  image_file=$(find $1 -maxdepth 1 -type f -name "*.jpg" -print -quit)

  if [ -z "$image_file" ]; then
      echo "no image found in volume"
      exit 1
  fi


  #run detection script
  python ./src/ocrModel.py "$image_file"

  # Signal completion
  touch /usr/app/status/alphanumeric.done

  echo "Alphanumeric tasks completed. Waiting for reset..."

  # Wait for reset signal
  while [ ! -f /usr/app/status/reset.done ]; do
    sleep 0.1
  done

  # Reset status
  rm /usr/app/status/alphanumeric.done /usr/app/status/reset.done
done