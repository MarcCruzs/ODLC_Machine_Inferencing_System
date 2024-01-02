from PIL import Image, ImageDraw
import os, random, datetime, string

# sets path for bg and fg folders on harddrive
BG_PATH = "E:\\2023\\synthetic_data_collection\\background"
FG_PATH = "E:\\2023\\circles_only"

# Pre-defines Yolo Class numbers
SHAPE_YOLO_CLASS_NUMBERS = {
    "star": 0,
    "cross": 1,
    "pentagon": 2,
    "triangle": 3,
    "rectangle": 4,
    "quartercircle": 5,
    "semicircle": 6,
    "circle": 7,
}

# minimum scaling that is still human readable
SCALING_CONSTANTS = {
    "star": 0.045,
    "cross": 0.0275,
    "pentagon": 0.035,
    "triangle": 0.035,
    "rectangle": 0.0275,
    "quartercircle": 0.0275,
    "semicircle": 0.02125,
    "circle": 0.02625,
}


def get_scaling(name: str) -> float:
    """Gets random scale factor for images (soon to be deprecated)

    Args:
        name (str): name of shape

    Returns:
        float: randomly generated scale factor between a range
    """
    upper = 0.05
    lower = 0.45

    name = name.split("_")[1]

    lower = SCALING_CONSTANTS[name]
    return random.uniform(lower, upper)


def add_bounding_box(
    im: Image, color: str = "Yellow", margin: int = 5, draw_box: bool = False
) -> Image:
    """Adds bounding box to foreground image in YOLO format through resizing.
    Can include physical box as well

    Args:
        im (Image): Image to get bounding box applied to
        color (str, optional): Color of drawn bounding box
        margin (int, optional): Margin between box and image. Defaults to 5.
        draw_box (bool, optional): If physical box should also be drawn. Defaults to False.

    Returns:
        Image: New image with bounding box pasted
    """
    new_im = Image.new(
        "RGBA", (im.size[0] + 2 * margin, im.size[1] + 2 * margin), (0, 0, 0, 0)
    )
    new_im.paste(im, (margin, margin))
    w, h = new_im.size

    if draw_box:
        draw = ImageDraw.Draw(new_im)
        draw.line((0, 0, 0, h), fill=color, width=3)
        draw.line((w, 0, w, h), fill=color, width=3)
        draw.line((0, 0, w, 0), fill=color, width=3)
        draw.line((0, h, w, h), fill=color, width=3)
    return new_im


def get_random_color():
    colors = ["white", "black", "red", "blue", "green", "purple", "brown", "orange"]
    return random.choice(colors)


# run in debugger or cmd or something
for file in os.listdir(FG_PATH):
    # gets random image from random subfolder of base path
    # rand_subfolder = os.path.join(BG_PATH, random.choice(os.listdir(BG_PATH)))
    # rand_bg = os.path.join(rand_subfolder, random.choice(os.listdir(rand_subfolder)))
    # rand_fg = os.path.join(FG_PATH, random.choice(os.listdir(FG_PATH)))
    rand_bg = "E:\\2023\\synthetic_data_collection\\background\\a000\\Video_Breakdown43281.png"
    rand_fg = os.path.join(FG_PATH, file)

    # skips images whose text is same color as shape color
    img_name = os.path.basename(rand_fg)
    image_name = img_name.split(".")[0]
    image_name = image_name.split("_")
    if image_name[0] == image_name[-1]:
        continue

    # opens the images
    background = Image.open(rand_bg)
    foreground = Image.open(rand_fg)

    # scales down shapes
    scale_factor = get_scaling(os.path.basename(img_name))
    foreground = foreground.resize(
        (
            int(foreground.size[0] * scale_factor),
            int(foreground.size[1] * scale_factor),
        ),
        resample=Image.BILINEAR,
    )

    # gets image dimensions
    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size

    # sets boundaries to prevent image from going outside the view
    max_x = bg_width - (fg_width + 10)
    max_y = bg_height - (fg_height + 10)

    # gets a random coordinate value that is less than the max
    coords = (random.randint(0, max_x), random.randint(0, max_y))

    now = datetime.datetime.now()
    formatted_now = now.strftime("%f")

    foreground = add_bounding_box(foreground, "Yellow")
    upper_left = coords
    lower_right = (coords[0] + foreground.size[0], coords[1] + foreground.size[1])
    box_coords = upper_left + lower_right

    # creates 12 images, each rotated 30 degrees more than the previous
    width, height = foreground.size
    for j in range(12):
        rotation = j * 30
        new_bg = background.copy()
        new_fg = foreground.rotate(rotation, expand=True, resample=Image.BICUBIC)
        new_bg.paste(new_fg, coords, new_fg)
        fg_center = (coords[0] + new_fg.size[0] / 2, coords[1] + new_fg.size[1] / 2)
        # generates unique image name
        new_filename = (
            rand_fg.split("\\")[-1].split(".")[0]
            + "_"
            + rand_bg.split("\\")[-1].split(".")[0]
        )
        coord_file = (
            new_filename + "-" + str(rotation) + "_" + str(formatted_now) + ".txt"
        )
        new_filename += "-" + str(rotation) + "_" + str(formatted_now) + ".png"
        new_bg.save(
            f"E:\\2023\\synthetic_data_collection\\combined_images\\{new_filename}",
            "PNG",
        )
        with open(
            f"E:\\2023\\synthetic_data_collection\\combined_images\\{coord_file}", "w"
        ) as f:
            name = os.path.basename(img_name).split("_")[1]
            res = (
                str(SHAPE_YOLO_CLASS_NUMBERS[name])
                + " "
                + str(fg_center[0] / bg_width)
                + " "
                + str(fg_center[1] / bg_height)
                + " "
            )
            res += str(width / bg_width) + " " + str(height / bg_height)
            f.write(res)
print("Done")


# TODO: implement what marc said, shown below
"""
Marc was basically saying that of that super chinese dataset he gave me, find one that is 90 feet in the air
and get a scaling for that, then get an error margin, so it would be like 0.05 +- 0.02 or something
"""
