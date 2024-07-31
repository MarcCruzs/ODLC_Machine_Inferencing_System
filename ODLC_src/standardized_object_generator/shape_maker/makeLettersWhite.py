import glob
import os

from PIL import (
    Image,
    ImageColor,
)


def replace_color(image_path, target_color="black", replacement_color="white"):
    # Convert colors to RGB tuples
    target_rgb = ImageColor.getrgb(target_color)
    replacement_rgb = ImageColor.getrgb(replacement_color)

    # Load the image
    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            if (r, g, b) == target_rgb:
                pixels[x, y] = replacement_rgb + (a,)  # Replace with the new color and maintain original alpha

    return img


lettersFilePath = glob.glob(r"C:\Users\jcmis\Downloads\School\UAV Lab\letters\*")


for letter in lettersFilePath:
    letterFileName = os.path.basename(letter)

    whiteLetter = replace_color(letter, "black", "white")
    whiteLetter.save(rf"whiteLetters\{letterFileName}")


# print(os.path.basename(file))
