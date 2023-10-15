# Imports PIL module
import string, shapesModule

shapes = [
    "circle",
    "semicircle",
    "quartercircle",
    "rectangle",
    "triangle",
    "pentagon",
    "star",
    # "cross",
]

colors = ["white", "black", "red", "blue", "green", "purple", "brown", "orange"]
numbers = list(range(1, 10))
alphabet = list(string.ascii_uppercase)


for shape in shapes:
    for color in colors:


        match shape:
            case "circle":
                img = shapesModule.createCircle(color)

            case "rectangle":
                img = shapesModule.createRectangle(color)
            
            case "triangle":
                img = shapesModule.createPolygon(color, 3)
            case "pentagon":
                img = shapesModule.createPolygon(color, 5)
            
            case "semicircle":
                shapesModule.createSemiCircles(color)
                #images are created within function

            case "quartercircle":
                shapesModule.createQuarterCircles(color)
                #images are created within function

            case "star":

                starBaseImagePath = "C:\\Users\\jcmis\\Downloads\\School\\UAV Lab\\baseImages\\starOutlineWhite.png"
                coloredStar = shapesModule.replace_white_with_color(starBaseImagePath, color)

                img = coloredStar

        if shape != "semicircle" and shape != "quartercircle":
            img = img.resize((500, 500), 5)
            img.save(f"testImages/{color}_{shape}.png", quality=100)


