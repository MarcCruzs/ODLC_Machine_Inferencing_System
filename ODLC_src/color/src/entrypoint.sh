#!/bin/bash

while true; do
  # Wait for shape human to complete
  while [ ! -f /usr/app/status/shape_human.done ]; do
    echo "Waiting for shape human to complete..."
    sleep 0.1
  done

  # Color tasks
  echo "Running color tasks..."

  #get an image from volume 1
  image_file=$(find $1 -maxdepth 1 -type f -name "*.jpg" -print -quit)

  if [ -z "$image_file" ]; then
      echo "no image found in volume"
      exit 1
  fi


  #run detection script
  python ./src/TextAndColorDet.py "$image_file"

  # Signal completion
  touch /usr/app/status/color.done

  echo "Color tasks completed. Waiting for reset..."

  # Wait for reset signal
  while [ ! -f /usr/app/status/reset.done ]; do
    sleep 0.025
  done

  # Reset status
  rm /usr/app/status/color.done /usr/app/status/reset.done
done