import datetime
import os
import random
import string
import time

from PIL import Image

start_time = time.time()

BG_PATH = "/data03/home/jestrada2/synthetic_data_collection/solid_color_bg"
FG_PATH = "/data03/home/jestrada2/synthetic_data_collection/targetsWithAlphaNum"

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

# manually tweaked and tested with 2 people to find minimum scaling factor that is still human readable
# SCALING_CONSTANTS = {
#     'star': 0.045, 'cross': 0.0275, 'pentagon': 0.035, 'triangle': 0.035, 'rectangle': 0.0275,
#     'quartercircle': 0.0275, 'semicircle': 0.02125, 'circle': 0.02625
# }


def lower_quality(pilImage):
    origW, origH = pilImage.size
    blur_factor = random.randint(19, 26)
    blurred = pilImage.resize((blur_factor, blur_factor))
    blurred = blurred.resize((origW, origH))

    return blurred


def get_scaling(name):
    upper = 20.37
    lower = 15.63

    return random.uniform(lower, upper)


def add_bounding_box(im, color, margin=5):
    new_im = Image.new("RGBA", (im.size[0] + 2 * margin, im.size[1] + 2 * margin), (0, 0, 0, 0))
    new_im.paste(im, (margin, margin))
    w, h = new_im.size

    # draw = ImageDraw.Draw(new_im)
    # draw.line((0, 0, 0, h), fill=color, width=3)
    # draw.line((w, 0, w, h), fill=color, width=3)
    # draw.line((0, 0, w, 0), fill=color, width=3)
    # draw.line((0, h, w, h), fill=color, width=3)
    return new_im


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_uppercase + string.digits
    result_str = "".join(random.choice(letters_and_digits) for i in range(length))
    return result_str


def get_random_color():
    colors = ["white", "black", "red", "blue", "green", "purple", "brown", "orange"]
    return random.choice(colors)


# run in debugger or cmd or something
count_stop = 0
for file in os.listdir(FG_PATH):
    count_stop += 1
    if count_stop >= 1000:
        break
    # gets random image from random subfolder of base path
    # rand_subfolder = os.path.join(BG_PATH, random.choice(os.listdir(BG_PATH)))
    # rand_bg = os.path.join(rand_subfolder, random.choice(os.listdir(rand_subfolder)))
    rand_fg = os.path.join(FG_PATH, random.choice(os.listdir(FG_PATH)))
    rand_bg = os.path.join(BG_PATH, random.choice(os.listdir(BG_PATH)))

    # skips images whose text is same color as shape color
    img_name = os.path.basename(rand_fg)
    image_name = img_name.split(".")[0]
    image_name = image_name.split("_")
    if image_name[0] == image_name[-1]:
        continue

    # opens the images
    background = Image.open(rand_bg)
    foreground = Image.open(rand_fg)
    foreground = lower_quality(foreground)

    # scales down shapes
    new_size = get_scaling(os.path.basename(img_name))
    foreground = foreground.resize(
        (
            int(new_size / 2 * 2),
            int(new_size / 2 * 2),
        ),
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
        new_filename = rand_fg.split("/")[-1].split(".")[0] + "_" + rand_bg.split("/")[-1].split(".")[0]
        coord_file = new_filename + "-" + str(rotation) + "_" + str(formatted_now) + ".txt"
        new_filename += "-" + str(rotation) + "_" + str(formatted_now) + ".png"
        new_bg.save(
            f"/data03/home/jestrada2/synthetic_data_collection/unc_dataset/images/{new_filename}",
            "PNG",
        )
        with open(
            f"/data03/home/jestrada2/synthetic_data_collection/unc_dataset/labels/{coord_file}",
            "w",
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
end_time = time.time()
time_taken = end_time - start_time
hours, remainder = divmod(time_taken, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Time taken to complete: **{int(hours)} hours, {int(minutes)} minutes, {round(seconds, 2)} seconds**")
