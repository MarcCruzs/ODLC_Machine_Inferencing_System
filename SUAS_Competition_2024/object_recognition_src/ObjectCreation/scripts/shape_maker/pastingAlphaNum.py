import os
import glob
import shapesModule
# Imports PIL module
import PIL
from PIL import (
    Image,
    ImageDraw,
    ImageColor,
    ImageMorph,
    ImageFilter,
    ImagePath,
    ImageFont,
)
import math
def paste_letter_on_image(img, letter_img_path):
    # Load the letter image
    letter_img = Image.open(letter_img_path)

    # Compute position to center the letter image on the main image
    x = (img.width - letter_img.width) / 2
    y = (img.height - letter_img.height) / 2

    # Paste the letter image onto the main image at the computed position
    # The fourth parameter is the alpha channel which makes sure transparency is preserved
    img.paste(letter_img, (int(x), int(y)), letter_img)

    return img

 # Adjust this list to your actual paths





shapes = glob.glob(r"C:\Users\jcmis\Downloads\School\UAV Lab\shapes\*")
blackLetters = glob.glob(r"C:\Users\jcmis\Downloads\School\UAV Lab\letters\*")
whiteLetters = glob.glob(r"C:\Users\jcmis\Downloads\School\UAV Lab\whiteLetters\*")

for shape in shapes:
    for letter in whiteLetters:

        shapeName = os.path.basename(shape)
        shapeColor = shapeName[0:5]

        shapeImage = Image.open(shape)
        croppedImage = shapesModule.crop_transparent(shapeImage)

        if shapeColor == "white":
            blackLetterPath = os.path.basename(letter)
            letter_path = os.path.join(r"C:\Users\jcmis\Downloads\School\UAV Lab\letters", blackLetterPath)
        else:
            letter_path = letter

        # Open and resize the letter image
        letterImage = Image.open(letter_path)
        new_width = letterImage.width - 70
        new_height = letterImage.height - 70
        letterImage = letterImage.resize((new_width, new_height), PIL.Image.LANCZOS)

        # Compute paste position to center the letter on croppedImage
        paste_x = (croppedImage.width - new_width) // 2
        paste_y = (croppedImage.height - new_height) // 2
        croppedImage.paste(letterImage, (paste_x, paste_y), letterImage)  # Using the alpha channel of letterImage for pasting

        croppedImage.save(f"D:/targetsWithAlphaNum/{shapeName}_{os.path.basename(letter)}")


#print(os.path.basename(file))
