import PIL, math, shapesModule
from PIL import (
    Image,
    ImageDraw,
    ImageColor,
    ImageMorph,
    ImageFilter,
    ImagePath,
    ImageFont,
)
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

blackCross = Image.open(r"C:\Users\jcmis\Downloads\School\UAV Lab\GitRepo\SUAS_Competiton\SUAS_Competition_2024\object_recognition_src\ObjectCreation\baseImages\newBlackCross.png")
whiteCross = Image.open(r"C:\Users\jcmis\Downloads\School\UAV Lab\GitRepo\SUAS_Competiton\SUAS_Competition_2024\object_recognition_src\ObjectCreation\baseImages\newWhiteCross.png")

# Resize the white cross to ensure a 20-pixel border
smallWC = whiteCross.resize((490,490), Image.LANCZOS)

# Calculate the offset to paste the white cross centered on the black cross
x_offset = (blackCross.width - smallWC.width) // 2
y_offset = (blackCross.height - smallWC.height) // 2

# Paste the smaller white cross onto the black cross
blackCross.paste(smallWC, (5, 5), smallWC)  # Assuming the white cross has transparency
blackCross.show()