from PIL import Image
import matplotlib.pyplot as plt
import cv2

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


def adjust_contrast_brightness(img, contrast: float = 1.0, brightness: int = 0):
    """
    Adjusts contrast and brightness of a uint8 image.
    contrast: (0.0, inf) with 1.0 leaving the contrast as is
    brightness: [-255, 255] with 0 leaving the brightness as is
    """
    brightness += int(round(255 * (1 - contrast) / 2))
    return cv2.addWeighted(img, contrast, img, 0, brightness)


def closest_color(requested_color: list) -> str:
    """This function gets the closest color name to an rgb value. For example:
    we know rgb(0,0,0) is black and rgb(0,0,255) is blue, if we get an unknown
    rgb value, this function would get the closest corresponding color name based
    on a pre-defined list of SUAS-allowed colors.

    Args:
        requested_color (list): RGB value

    Returns:
        String: Corresponding color name for the RGB value
    """
    min_colors = {}
    for color_name, color_rgb in COLORS.items():
        rd = (color_rgb[0] - requested_color[0]) ** 2
        gd = (color_rgb[1] - requested_color[1]) ** 2
        bd = (color_rgb[2] - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = color_name
    return min_colors[min(min_colors.keys())]


# Open the image
image_path = r"C:\Users\joshu\OneDrive\Documents\VsCode\SUAS_Competition\SUAS_Competiton\SUAS_Competition_2024\object_recognition_src\ObjectCreation\testImages\blue_pentagon_M_purple.png"
im = cv2.imread(image_path, 1)
plt.imshow(im)
plt.show()
height, width, _ = im.shape

# Calculate the coordinates for cropping
x1 = (width - 300) // 2
y1 = (height - 300) // 2
x2 = x1 + 300
y2 = y1 + 300

# Crop the middle region
cropped = im[y1:y2, x1:x2]
plt.imshow(cropped)
plt.show()
adjusted = adjust_contrast_brightness(cropped, 2.5, -100)

rgb_image = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
pil_img = Image.fromarray(rgb_image)
plt.imshow(pil_img)
plt.show()
# Quantize down to 2-color palettized image using "Fast Octree" method
q = pil_img.quantize(colors=2, method=2)
plt.imshow(q)
plt.show()
# Get the first 2 colors (each represented by 3 RGB entries) from the palette
colors = q.getpalette()[:6]
# colors = [color for color in colors]
# Interpret the colors
print(f"First color: RGB {colors[:3]} =", closest_color(colors[:3]))
print(f"Second color: RGB {colors[3:]} =", closest_color(colors[3:]))
