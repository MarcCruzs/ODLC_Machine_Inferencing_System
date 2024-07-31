# built-in python library for writing cmd scripts
import argparse
import time

import cv2
import matplotlib.pyplot as plt
from PIL import Image

COLORS = {
    "red": (172, 0, 0),
    "green": (0, 172, 0),
    "blue": (0, 0, 172),
    "black": (-50, -50, -50),
    "purple": (128, 0, 128),
    "white": (255, 255, 255),
    "orange": (255, 165, 0),
    "brown": (150, 75, 0),
}


def display_rgb_image(img: Image) -> None:
    """Wrapper function for matplotlib's image display functions.
    Simplifies the overall thing to a one-liner

    Args:
    ----
        img (Image): PIL Image or OpenCV Image converted to rgb format (default is bgr)

    """
    plt.imshow(img)
    plt.axis("off")
    plt.show()


def adjust_contrast_brightness(img: Image, contrast: float = 1.0, brightness: int = 0) -> Image:
    """Adjusts the contrast and brightness of a PIL or converted OpenCV image.

    Args:
    ----
        img (Image): The input image.
        contrast (float): The contrast adjustment factor. A value of 1.0 leaves the contrast as is.
            Values greater than 1.0 increase the contrast, while values less than 1.0 decrease the contrast.
        brightness (int): The brightness adjustment value. A value of 0 leaves the brightness as is.
            Values greater than 0 increase the brightness, while values less than 0 decrease the brightness.

    Returns:
    -------
        Image: The adjusted image.

    """
    brightness += int(round(255 * (1 - contrast) / 2))
    return cv2.addWeighted(img, contrast, img, 0, brightness)


def closest_color(requested_color: list) -> str:
    """This function gets the closest color name to an rgb value. For example:
    we know rgb(0,0,0) is black and rgb(0,0,255) is blue, if we get an unknown
    rgb value, this function would get the closest corresponding color name based
    on a pre-defined list of SUAS-allowed colors.

    Args:
    ----
        requested_color (list): RGB value

    Returns:
    -------
        String: Corresponding color name for the RGB value

    """
    min_colors = {}
    for color_name, color_rgb in COLORS.items():
        rd = (color_rgb[0] - requested_color[0]) ** 2
        gd = (color_rgb[1] - requested_color[1]) ** 2
        bd = (color_rgb[2] - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = color_name
    return min_colors[min(min_colors.keys())]


parser = argparse.ArgumentParser(description="Process an Image file.")
parser.add_argument("ImagePath", metavar="path", type=str, help="the path to an image file")
args = parser.parse_args()

if args.ImagePath is None:
    print("Please provide the path to an image file.")
    exit()

start_time = time.time()
im = cv2.imread(args.ImagePath, 1)


height, width, _ = im.shape

# Calculate the coordinates for cropping
x1 = (width - 300) // 2
y1 = (height - 300) // 2
x2 = x1 + 300
y2 = y1 + 300

# Crop the middle region
cropped = im[y1:y2, x1:x2]


adjusted = adjust_contrast_brightness(cropped, 3, -120)

rgb_image = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
pil_img = Image.fromarray(rgb_image)
result = pil_img.point(lambda i: (i - 70) * 255 / (255 - 70) if (i > 70) else 0)
pil_img = result


# Quantize down to 2-color palettized image using "Fast Octree" method
q = pil_img.quantize(colors=2, method=2)
end_time = time.time()

# Get the first 2 colors (each represented by 3 RGB entries) from the palette
colors = q.getpalette()[:6]

# Interpret the colors
print(f"Shape color: RGB {colors[:3]} =", closest_color(colors[:3]))
print(f"Text color: RGB {colors[3:]} =", closest_color(colors[3:]))

print(f"The script took {end_time-start_time:.5f} seconds to run.")
