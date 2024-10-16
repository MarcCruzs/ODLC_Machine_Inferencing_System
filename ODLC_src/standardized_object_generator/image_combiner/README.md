# Image Combiner Documentation

## Description

The script sets two paths for the background and foreground images, respectively, using the variables BG_PATH and FG_PATH. These paths are hardcoded to specific directories located on an external harddrive

The script then iterates over all the foreground images. Within the loop, it selects a random subfolder and image from the background path using the os module, and a random image from the foreground path using the random module.

The script checks if the text color of the foreground image is the same as the shape color. If it is, the loop skips that image. If not, it opens the background and foreground images using the Image module.

The script scales down the foreground image by a random factor between 3.5% and 10% using the resize() method of the Image module to mimic the UAV altitude range of 65-85ft. It then gets the dimensions of the background and foreground images using the size attribute of the Image module.

Then, by getting a random coordinate within the boundary calculated based on the dimensions of the image, it overlays the foreground onto the background. Afterwards, the foreground gets placed in the same spot 12 different times but with 30 degree rotations each time. So it would start from 0 degrees, then 30, all the way up to 330 degrees. The script also generates a unique name for the combined image that contains information like shape, text, and color. 
