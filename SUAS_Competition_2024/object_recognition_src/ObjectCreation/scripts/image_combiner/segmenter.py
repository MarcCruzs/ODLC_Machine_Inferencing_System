import cv2, os
import numpy as np

DIRECTORY = 'E:/2023/synthetic_data_collection/background'

# Divides every background in the backgrounds folder into 16 pieces
for filename in os.listdir(DIRECTORY):
    # Load the image
    image = cv2.imread(os.path.join(DIRECTORY, filename))

    # Get the height and width of the image
    height, width, _ = image.shape

    # Calculate the segment height and width
    seg_height, seg_width = int(height/np.sqrt(16)), int(width / np.sqrt(16))

    # counts up to 16 to prevent weird cases with differing image sizes
    count = 0
    # Loop over the image
    for i in range(0, height, seg_height):
        for j in range(0, width, seg_width):
            # cutoff point of 16 because after 16, it only gets small slivers of the image
            if count > 15:
                break
            # Create a new image segment
            segment = image[i:i+seg_height, j:j+seg_width]
            
            # Save each segment to a file
            cv2.imwrite(f'E:/2023/synthetic_data_collection/segmented/{filename}_segment_{i}_{j}.jpg', segment)
            count += 1