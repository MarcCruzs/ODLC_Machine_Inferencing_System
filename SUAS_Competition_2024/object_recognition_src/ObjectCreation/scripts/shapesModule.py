import PIL, math
from PIL import (
    Image,
    ImageDraw,
    ImageColor,
    ImageMorph,
    ImageFilter,
    ImagePath,
    ImageFont,
)

shapePath = ("D:/targetsWithAlphaNum")
font_path = r"C:\Users\jcmis\Downloads\School\UAV Lab\fonts\coolvetica condensed rg.otf"


def createQuarterCircles(color, characterColor, text):
    w, h = 1000, 1000
    radius_outer = 470  # Outermost radius for the border
    radius_inner = radius_outer - 10  # Radius for the inner semicircle
    # Define the bounding boxes
    shape_outer = [
        (w / 2 - radius_outer, h / 2 - radius_outer),
        (w / 2 + radius_outer, h / 2 + radius_outer),
    ]
    shape_inner = [
        (w / 2 - radius_inner, h / 2 - radius_inner),
        (w / 2 + radius_inner, h / 2 + radius_inner),
    ]

    # Line for the border on the flat side
    line_end = (w / 2 + radius_inner + 10, h / 2)

    line_end2 = (w/2 -5, h -30 )

    # Creating new Image object
    img = Image.new("RGBA", (w, h))

    # Drawing
    draw = ImageDraw.Draw(img)
    draw.pieslice(shape_outer, start=0, end=90, fill="black")  # Border semicircle
    draw.pieslice(shape_inner, start=0, end=90, fill=color)  # Inner semicircle
    
    #horizontal line
    draw.line(
        [(491, 500), line_end], fill="black", width=10
    )

    #vertical line
    draw.line(
        [(495,500), line_end2], fill="black", width=10
    )  

    img1Num = returnShapeWithCharacter(img, "quartercircle", "bottomRight", characterColor,text)

    img1Num.save(f"{shapePath}/{color}_quartercircle_bottomRight_{text}_{characterColor}.png", quality=100)

    img2 = Image.new("RGBA", (w,h))
    img2 = img.rotate(90, PIL.Image.NEAREST, expand = 1)
    img2Num = returnShapeWithCharacter(img2, "quartercircle", "topRight", characterColor,text)
  
    img2Num.save(f"{shapePath}/{color}_quartercircle_topRight_{text}_{characterColor}.png", quality=100)

    img3 = Image.new("RGBA", (w,h))
    img3 = img.rotate(180, PIL.Image.NEAREST, expand = 1)
    img3Num = returnShapeWithCharacter(img3, "quartercircle", "topLeft", characterColor,text)
    
    img3Num.save(f"{shapePath}/{color}_quartercircle_topLeft_{text}_{characterColor}.png", quality=100)

    img4 = Image.new("RGBA", (w,h))
    img4 = img.rotate(270, PIL.Image.NEAREST, expand = 1)
    img4Num = returnShapeWithCharacter(img4, "quartercircle", "bottomLeft", characterColor,text)
    
    img4Num.save(f"{shapePath}/{color}_quartercircle_bottomLeft_{text}_{characterColor}.png", quality=100)


def createSemiCircles(color, characterColor,text):
    w, h = 1000, 1000
    radius_outer = 470  # Outermost radius for the border
    radius_inner = radius_outer - 10  # Radius for the inner semicircle
    
    # Define the bounding boxes
    shape_outer = [(w/2 - radius_outer, h/2 - radius_outer), (w/2 + radius_outer, h/2 + radius_outer)]
    shape_inner = [(w/2 - radius_inner, h/2 - radius_inner), (w/2 + radius_inner, h/2 + radius_inner)]

    # Line for the border on the flat side
    line_start = (w/2 - radius_inner -10, h/2)
    line_end = (w/2 + radius_inner +10, h/2)

    # Creating new Image object
    img = Image.new("RGBA", (w, h))
    
    # Drawing
    draw = ImageDraw.Draw(img)
    draw.pieslice(shape_outer, start = 0, end = 180, fill="black")  # Border semicircle
    draw.pieslice(shape_inner, start = 0, end = 180, fill=color)  # Inner semicircle
    draw.line([line_start, line_end], fill="black", width=10)  # Line for the flat side's border
    
    
    img1Num = returnShapeWithCharacter(img, "semicircle", "bottom", characterColor,text)
    img1Num.save(f"{shapePath}/{color}_semicircle_bottom_{text}_{characterColor}.png", quality=100)

    img2 = Image.new("RGBA", (w,h))
    img2 = img.rotate(90, PIL.Image.NEAREST, expand = 1)
    img2Num = returnShapeWithCharacter(img2, "semicircle", "bottom", characterColor,text)
    img2Num.save(f"{shapePath}/{color}_semicircle_right_{text}_{characterColor}.png", quality=100)

    img3 = Image.new("RGBA", (w,h))
    img3 = img.rotate(180, PIL.Image.NEAREST, expand = 1)
    img3Num = returnShapeWithCharacter(img3, "semicircle", "bottom", characterColor,text)
    img3Num.save(f"{shapePath}/{color}_semicircle_top_{text}_{characterColor}.png", quality=100)

    img4 = Image.new("RGBA", (w,h))
    img4 = img.rotate(270, PIL.Image.NEAREST, expand = 1)
    img4Num = returnShapeWithCharacter(img4, "semicircle", "bottom", characterColor,text)
    img4Num.save(f"{shapePath}/{color}_semicircle_left_{text}_{characterColor}.png", quality=100)




def createPolygon(color, sides):
    radius_outer = 490  # Radius for the outer (border) pentagon
    radius_inner = radius_outer - 10  # Radius for the inner pentagon
    cx, cy = 500, 500  # center of the canvas
    
    xy_outer = [(cx + radius_outer * math.cos(th), cy + radius_outer * math.sin(th)) for th in [i * (2 * math.pi) / sides for i in range(sides)]]
    xy_inner = [(cx + radius_inner * math.cos(th), cy + radius_inner * math.sin(th)) for th in [i * (2 * math.pi) / sides for i in range(sides)]]
    
    pentagon = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    draw = ImageDraw.Draw(pentagon)
    draw.polygon(xy_outer, fill="black")  # Drawing the border pentagon
    draw.polygon(xy_inner, fill= color)  # Drawing the inner pentagon
    
    pentagon = pentagon.resize((200, 200), 5)  # Using Image.LANCZOS for a higher-quality downscaling
    pentagon = pentagon.rotate(90, PIL.Image.NEAREST, expand = 1)
    return pentagon

def createRectangle(color):
    rectangle = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))

    draw = ImageDraw.Draw(rectangle)
# Draw the outermost black rectangle for the border
    draw.rectangle((0, 0, 1000, 1000), fill="black")


    draw.rectangle((10, 10, 990, 990), fill=color)

    return rectangle

def createCircle(color):
    img = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    draw.ellipse([(0, 0), (1000, 1000)], fill="black")  # Outermost border
    draw.ellipse([(10, 10), (990, 990)], fill=color)  

    return img

def replace_white_with_color(image_path, replacement_color):
    # Load the image
    newColor = ImageColor.getrgb(replacement_color)
    img = Image.open(image_path)
    img = img.convert("RGBA")
    pixels = img.load()

    # Define what we consider "white" (you can tweak these values)
    # The closer the threshold is to 255, the stricter the replacement will be
    threshold = 245  

    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            if r > threshold and g > threshold and b > threshold:
                pixels[x, y] = newColor + (a,) 

    return img

def replace_all_colors_with_new(image_path, replacement_color):
    # Load the image
    newColor = ImageColor.getrgb(replacement_color)
    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = img.getpixel((x, y))
            if a > 0:  # Check if pixel is not transparent
                pixels[x, y] = newColor + (a,)  # Replace only RGB, keep alpha (transparency) the same

    return img

def crop_transparent(img):
    """
    Crop the transparent borders from an image and return the cropped image.
    """
    # Convert the image to RGBA if it's not already
    img = img.convert("RGBA")
    
    # Get the pixels of the image as a list
    datas = img.getdata()
    
    # Lists to store non-transparent pixel coordinates
    non_transparent_xs = []
    non_transparent_ys = []

    # Loop through each pixel in the image
    for y in range(img.height):
        for x in range(img.width):
            if datas[y * img.width + x][3] > 0:  # If alpha channel > 0 (i.e., not transparent)
                non_transparent_xs.append(x)
                non_transparent_ys.append(y)

    # Get the bounding box (left, upper, right, lower) of the non-transparent region
    box = (min(non_transparent_xs), min(non_transparent_ys), max(non_transparent_xs), max(non_transparent_ys))

    # Crop the image using the bounding box
    cropped_img = img.crop(box)

    return cropped_img

def returnShapeWithCharacter(img, shape, orientation, characterColor, text):
    fontSize = 500
    Horoffset = 0
    Veroffset = 10
    if shape == "quartercircle":
        fontSize = 400
        match orientation:
            case "topLeft":
                Horoffset = 10
                Veroffset = 25
            case "topRight":
                Horoffset = -30
                Veroffset = 25
            case "bottomLeft":
                Horoffset = 40
                Veroffset = -15
            case "bottomRight":
                Horoffset = -30
                Veroffset = 15
            case _:
                Horoffset = 0
                Veroffset = 0


    img = crop_transparent(img)
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
    if shape != "semicircle":
        img = img.resize((500, 500), 5)
    return img