#!/bin/bash

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