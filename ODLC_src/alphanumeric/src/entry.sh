#!/bin/bash

#get an image from volume 1
image_file=$(find $1 -maxdepth 1 -type f -name "*.jpg" -print -quit)

if [ -z "$image_file" ]; then
    echo "no image found in volume"
    exit 1
fi


#run detection script
python ./src/ocrModel.py "$image_file"