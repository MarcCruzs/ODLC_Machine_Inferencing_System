import numpy as np
import cv2
import argparse
import os

# Define the command-line arguments
parser = argparse.ArgumentParser(description="Generate random images.")
parser.add_argument("--width", type=int, required=True, help="The width of the images.")
parser.add_argument(
    "--height", type=int, required=True, help="The height of the images."
)
parser.add_argument(
    "--num_images", type=int, required=True, help="The number of images to generate."
)
parser.add_argument(
    "--output_dir", type=str, required=True, help="The directory to save the images."
)
args = parser.parse_args()

# Ensure the output directory exists
os.makedirs(args.output_dir, exist_ok=True)

# Generate and save the images
for i in range(args.num_images):
    # Generate a smaller image
    small_pixels = np.random.randint(
        low=0, high=256, size=(args.height // 10, args.width // 10, 3), dtype=np.uint8
    )
    small_image = cv2.cvtColor(small_pixels, cv2.COLOR_RGB2BGR)

    # Resize the image to create larger square pixels
    image = cv2.resize(
        small_image, (args.width, args.height), interpolation=cv2.INTER_NEAREST
    )
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    color = cv2.cvtColor(grayscale, cv2.COLOR_GRAY2BGR)

    # Save the images
    cv2.imwrite(os.path.join(args.output_dir, f"grayscale_{i}.png"), color)
