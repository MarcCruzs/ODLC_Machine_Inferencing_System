#!/bin/bash

# Check if the raw_images directory exists, if not create it
if [ ! -d "/usr/app/src/raw_images" ]; then
    mkdir /usr/app/src/raw_images
fi

# Copy the first .jpg file from the shared volume to raw_images
image_file=$(find /local_volume -maxdepth 1 -type f -name "*.jpg" -print -quit)
if [ -z "$image_file" ]; then
    echo "No image found in volume"
    exit 1 
fi
cp "$image_file" /usr/app/src/raw_images/

# Run the detection script
python ./src/detect.py --source /usr/app/src/raw_images/$(basename "$image_file") --weights ./src/HumanModel.pt --save-txt --name ModelResults

# Remove the image after processing
rm /usr/app/src/raw_images/$(basename "$image_file")

rm "$image_file"