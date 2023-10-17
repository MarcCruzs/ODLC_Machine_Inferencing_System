# Imports PIL module
import string, shapesModule,math
from PIL import (
    Image,
    ImageDraw,
    ImageColor,
    ImageMorph,
    ImageFilter,
    ImagePath,
    ImageFont,
)

shapes = [
    "pentagon",
    "star",
    "triangle",
    "quartercircle",
    "cross",
    "semicircle",
    "circle",
    "rectangle",
       
]

colors = ["white", "black", "red", "blue", "green", "purple", "brown", "orange"]
characterColors = ["white", "black", "red", "blue", "green", "purple", "brown", "orange"]
numbers = ["0","1","2","3","4","5","6","7","8","9"]
alphabet = list(string.ascii_uppercase)
completeCharacters = numbers + alphabet

shapePath = ("D:/targetsWithAlphaNum")
font_path = r"C:\Users\jcmis\Downloads\School\UAV Lab\fonts\coolvetica condensed rg.otf"

for shape in shapes:
    for color in colors:
        for characterColor in characterColors:
            for text in completeCharacters:
                fontSize = 400
                Horoffset = 0
                Veroffset = 0

                match shape:
                    case "circle":
                        img = shapesModule.createCircle(color)
                        fontSize = 800
                    case "rectangle":
                        fontSize = 800
                        img = shapesModule.createRectangle(color)
                    
                    case "triangle":
                        img = shapesModule.createPolygon(color, 3)
                        Veroffset = 25
                        fontSize = 100
                        
                    case "pentagon":
                        img = shapesModule.createPolygon(color, 5)
                        Veroffset = 20
                        fontSize = 100
                    
                    case "semicircle":
                        shapesModule.createSemiCircles(color, characterColor,text)
                        
                        
                        #images are created within function

                    case "quartercircle":
                        shapesModule.createQuarterCircles(color, characterColor,text)
                        #images are created within function

                    case "star":

                        starBaseImagePath = "C:\\Users\\jcmis\\Downloads\\School\\UAV Lab\\GitRepo\\SUAS_Competiton\\SUAS_Competition_2024\\object_recognition_src\\ObjectCreation\\baseImages\\starOutlineWhite.png"
                        coloredStar = shapesModule.replace_white_with_color(starBaseImagePath, color)

                        img = coloredStar
                        fontSize = 250
                        Veroffset = 20
                    
                    case "cross":
                        crossPath = "C:\\Users\\jcmis\\Downloads\\School\\UAV Lab\\GitRepo\\SUAS_Competiton\\SUAS_Competition_2024\\object_recognition_src\\ObjectCreation\\baseImages\\crossBorder.png"
                        coloredCross = shapesModule.replace_white_with_color(crossPath, color)

                        img = coloredCross

                    
                
                

                if shape != "semicircle" and shape != "quartercircle":
                    img = shapesModule.crop_transparent(img)
                    draw = ImageDraw.Draw(img)

                    
                    # Load a font
                    font = ImageFont.truetype(font_path, size=fontSize)  # Change size as needed
                    shapeText = text  # Numbers as text

                    bbox = draw.textbbox((0, 0), shapeText, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    half_img_width = img.width / 2
                    half_img_height = img.height / 2
                    
                    

                    position = (half_img_width - text_width / 2 + Horoffset, (half_img_height - text_height + Veroffset) )

                    # Draw the text onto the image
                    draw.text(position, shapeText, font=font, fill=characterColor) 
                    img = img.resize((500, 500), 5)
                    img.save(f"{shapePath}/{color}_{shape}_{shapeText}_{characterColor}.png", quality=100)

            

