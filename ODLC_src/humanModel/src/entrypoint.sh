#!/bin/bash

#get an image from volume 1
image_file=$(find /raw_images -maxdepth 1 -type f -name "*.jpg" -print -quit)

if [ -z "$image_file" ]; then
    echo "no image found in volume"
    exit 1
fi

#copy image to volume 2 and remove it from first volume
# cp "$image_file" /imagebank

# rm /raw_images/$(basename "$image_file")

#run detection script
python ./src/detect.py --source /raw_images/$(basename "$image_file") --weights ./src/HumanModel.pt --save-txt --name ModelResults