import shapesModule
import PIL
from PIL import Image, ImageDraw, ImageFont

# shapes = [
#     "circle",
#     "semicircle",
#     "quartercircle",
#     "rectangle",
#     "triangle",
#     "pentagon",
#     "star",
#     # "cross",
# ]
# color = "red"
# fileSavePath = r"C:\Users\jcmis\Downloads\School\UAV Lab\GitRepo\SUAS_Competiton\SUAS_Competition_2024\object_recognition_src\ObjectCreation\testImages"

# for shape in shapes:
#     match shape:
#         case "circle":
#             img = shapesModule.createCircle(color)

#         case "rectangle":
#             img = shapesModule.createRectangle(color)
        
#         case "triangle":
#             img = shapesModule.createPolygon(color, 3)
#         case "pentagon":
#             img = shapesModule.createPolygon(color, 5)
        
#         case "semicircle":
#             shapesModule.createSemiCircles(color)
#             #images are created within function

#         case "quartercircle":
#             shapesModule.createQuarterCircles(color)
#             #images are created within function

#         case "star":

#             starBaseImagePath = r"C:\Users\jcmis\Downloads\School\UAV Lab\GitRepo\SUAS_Competiton\SUAS_Competition_2024\object_recognition_src\ObjectCreation\baseImages\starOutlineWhite.png"
#             coloredStar = shapesModule.replace_white_with_color(starBaseImagePath, color)

#             img = coloredStar
#     if shape != "semicircle" and shape != "quartercircle":
#             img = img.resize((500, 500), 5)
#             img.save(f"{fileSavePath}/{color}_{shape}.png", quality=100)


img = Image.open(r"C:\Users\jcmis\Downloads\School\UAV Lab\GitRepo\SUAS_Competiton\SUAS_Competition_2024\object_recognition_src\ObjectCreation\testImages\red_triangle.png")

# Create a drawing context
img = shapesModule.crop_transparent(img)
# img = img.resize((500, 500))
draw = ImageDraw.Draw(img)

# Load a font
font_path = r"C:\Users\jcmis\Downloads\School\UAV Lab\fonts\coolvetica condensed rg.otf"
font = ImageFont.truetype(font_path, size=300)  # Change size as needed
text = "0"  # Numbers as text

bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

half_img_width = img.width / 2
half_img_height = img.height / 2

position = (half_img_width - text_width / 2, (half_img_height - text_height +30) )

# Draw the text onto the image
draw.text(position, text, font=font, fill="blue")  # Change fill color as needed

# Save or display the result
img.show()