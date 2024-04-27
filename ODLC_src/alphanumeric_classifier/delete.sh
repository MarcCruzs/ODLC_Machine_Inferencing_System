#!/bin/bash

image_file=$(find /raw_images -maxdepth 1 -type f -name "*.jpg" -print -quit)


#delete image from volume
rm /raw_images/$(basename "$image_file")