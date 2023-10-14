import PIL, math
from PIL import Image, ImageDraw, ImageColor


def createQuarterCircles(color):
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

    img = img.resize((500, 500), 5)
    img.save(f"shapes\{color}_quartercircle_bottom.png", quality=100)

    img2 = Image.new("RGBA", (w,h))
    img2 = img.rotate(90, PIL.Image.NEAREST, expand = 1)
    img2.save(f"shapes\{color}_quartercircle_right.png", quality=100)

    img3 = Image.new("RGBA", (w,h))
    img3 = img.rotate(180, PIL.Image.NEAREST, expand = 1)
    img3.save(f"shapes\{color}_quartercircle_top.png", quality=100)

    img4 = Image.new("RGBA", (w,h))
    img4 = img.rotate(270, PIL.Image.NEAREST, expand = 1)
    img4.save(f"shapes\{color}_quartercircle_left.png", quality=100)

def createSemiCircles(color):
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
    
    img = img.resize((500, 500), 5)
    img.save(f"shapes\{color}_semicircle_bottom.png", quality=100)

    img2 = Image.new("RGBA", (w,h))
    img2 = img.rotate(90, PIL.Image.NEAREST, expand = 1)
    img2.save(f"shapes\{color}_semicircle_right.png", quality=100)

    img3 = Image.new("RGBA", (w,h))
    img3 = img.rotate(180, PIL.Image.NEAREST, expand = 1)
    img3.save(f"shapes\{color}_semicircle_top.png", quality=100)

    img4 = Image.new("RGBA", (w,h))
    img4 = img.rotate(270, PIL.Image.NEAREST, expand = 1)
    img4.save(f"shapes\{color}_semicircle_left.png", quality=100)




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

    # Draw the inner rectangle with the given color, leaving a 20-pixel border
    draw.rectangle((10, 10, 990, 990), fill=color)

    return rectangle

def createCircle(color):
    img = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    draw.ellipse([(0, 0), (1000, 1000)], fill="black")  # Outermost border
    draw.ellipse([(10, 10), (990, 990)], fill=color)   # Inner circle leaving a 20-pixel wide border

    return img

def replace_white_with_color(image_path, replacement_color):
    # Load the image
    newColor = ImageColor.getrgb(replacement_color)
    img = Image.open(image_path)
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

