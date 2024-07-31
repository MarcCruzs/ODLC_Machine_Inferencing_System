# Imports PIL module
import math

import PIL
from PIL import (
    Image,
    ImageColor,
    ImageDraw,
)


def createRectangle(color):
    rectangle = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))

    draw = ImageDraw.Draw(rectangle)

    draw.rectangle((0, 0, 1000, 1000), fill=(color), outline=("black"))

    rectangle = rectangle.resize((200, 200), 5)
    rectangle.save("testImages/rectangleTest.png", quality=95)
    rectangle.show()
    return rectangle


def createPolygon(color, sides):
    radius_outer = 450  # Radius for the outer (border) pentagon
    radius_inner = radius_outer - 20  # Radius for the inner pentagon
    cx, cy = 500, 500  # center of the canvas

    xy_outer = [
        (cx + radius_outer * math.cos(th), cy + radius_outer * math.sin(th))
        for th in [i * (2 * math.pi) / sides for i in range(sides)]
    ]
    xy_inner = [
        (cx + radius_inner * math.cos(th), cy + radius_inner * math.sin(th))
        for th in [i * (2 * math.pi) / sides for i in range(sides)]
    ]

    img = Image.new("RGBA", (1000, 1000), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.polygon(xy_outer, fill="black")  # Drawing the border pentagon
    draw.polygon(xy_inner, fill=color)  # Drawing the inner pentagon

    img = img.resize((200, 200), Image.LANCZOS)  # Using Image.LANCZOS for a higher-quality downscaling
    img = img.rotate(90, PIL.Image.NEAREST, expand=1)
    img.save("testImages/pentagonTest.png", quality=95)
    img.show()


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


def createSemiCircle():
    w, h = 1000, 1000
    radius_outer = 470  # Outermost radius for the border
    radius_inner = radius_outer - 20  # Radius for the inner semicircle

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
    line_start = (w / 2 - radius_inner - 20, h / 2)
    line_end = (w / 2 + radius_inner + 20, h / 2)

    # Creating new Image object
    img = Image.new("RGBA", (w, h))

    # Drawing
    draw = ImageDraw.Draw(img)
    draw.pieslice(shape_outer, start=0, end=180, fill="black")  # Border semicircle
    draw.pieslice(shape_inner, start=0, end=180, fill="red")  # Inner semicircle
    draw.line([line_start, line_end], fill="black", width=20)  # Line for the flat side's border

    img.show()

    img3 = Image.new("RGBA", (w, h))
    img3 = img.rotate(90, PIL.Image.NEAREST, expand=1)
    img3.show()

    img3 = Image.new("RGBA", (w, h))
    img3 = img.rotate(180, PIL.Image.NEAREST, expand=1)
    img3.show()

    img3 = Image.new("RGBA", (w, h))
    img3 = img.rotate(270, PIL.Image.NEAREST, expand=1)
    img3.show()


def createQuarterCircles():
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

    line_end2 = (w / 2 - 5, h - 30)

    # Creating new Image object
    img = Image.new("RGBA", (w, h))

    # Drawing
    draw = ImageDraw.Draw(img)
    draw.pieslice(shape_outer, start=0, end=90, fill="black")  # Border semicircle
    draw.pieslice(shape_inner, start=0, end=90, fill="red")  # Inner semicircle

    # horizontal line
    draw.line([(491, 500), line_end], fill="black", width=10)

    # vertical line
    draw.line([(495, 500), line_end2], fill="black", width=10)

    img.show()

    img2 = Image.new("RGBA", (w, h))
    img2 = img.rotate(90, PIL.Image.NEAREST, expand=1)
    img2.show()

    img3 = Image.new("RGBA", (w, h))
    img3 = img.rotate(180, PIL.Image.NEAREST, expand=1)
    img3.show()

    img4 = Image.new("RGBA", (w, h))
    img4 = img.rotate(270, PIL.Image.NEAREST, expand=1)
    img4.show()


# Usage
# colored_image = replace_white_with_color("C:\\Users\\jcmis\\Downloads\\School\\UAV Lab\\baseImages\\starOutlineWhite.png", "orange")  # Replace white with red
# colored_image.save(f"testImages/test_test.png")
# colored_image.show()
# createRectangle("orange")
# createPolygon("red", 5)
# createSemiCircle()
createQuarterCircles()
