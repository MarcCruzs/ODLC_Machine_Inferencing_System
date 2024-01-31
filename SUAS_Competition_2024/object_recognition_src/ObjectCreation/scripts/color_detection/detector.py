import time
startTime = time.time()
from PIL import Image
from matplotlib import pyplot as plt
import argparse, json
import os.path

# use pre-defined rgb values for SUAS-specified colors
COLORS = {
    "red": (128, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 128),
    "black": (-50, -50, -50),
    "purple": (128, 0, 128),
    "white": (255, 255, 255),
    "orange": (255, 165, 0),
    "brown": (150, 75, 0),
}


def get_dominant_colors(
    pil_img: Image, palette_size: int = 16, max_colors: int = 6
) -> list:
    """Gets the dominant colors from an image. Makes use of K-Means Algorithm that
    Pillow uses internally its Palette function.

    Args:
        pil_img (Image): Pillow Image
        palette_size (int, optional): Number of colors it should detect. Defaults to 16.
        max_colors (int, optional): Number of colors returned. Defaults to 6.

    Returns:
        list: List of tuples containing dominant color rgb value and a dominance percentage
    """
    # Resize image to speed up processing
    img = pil_img.copy()
    img.thumbnail((200, 200))

    # Reduce colors (uses k-means internally)
    paletted = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), key=lambda x: x[0], reverse=True)

    total_pixels = img.size[0] * img.size[1]
    dominant_colors = []
    for i in range(max_colors):
        palette_index = color_counts[i][1]
        color_count = color_counts[i][0]
        color_percentage = round(color_count / total_pixels, 4)
        color = palette[palette_index * 3 : palette_index * 3 + 3]
        if color not in [c[0] for c in dominant_colors]:  # Skip adding duplicate colors
            dominant_colors.append((color, color_percentage))

    return dominant_colors


def closest_color(requested_color: list) -> str:
    """This function gets the closest color name to an rgb value. For example:
    we know rgb(0,0,0) is black and rgb(0,0,255) is blue, if we get an unknown
    rgb value, this function would get the closest corresponding color name based
    on a pre-defined list of SUAS-allowed colors.

    Args:
        requested_color (list): RGB value

    Returns:
        String: Corresponding color name for the RGB value
    """
    min_colors = {}
    for color_name, color_rgb in COLORS.items():
        rd = (color_rgb[0] - requested_color[0]) ** 2
        gd = (color_rgb[1] - requested_color[1]) ** 2
        bd = (color_rgb[2] - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = color_name
    return min_colors[min(min_colors.keys())]


# function to add to JSON
"""
JSON file must be predefined with
{

}
being the file, if not, it will break
"""


def write_json(new_data, timestamp, filename="colorOutputs.json"):
    with open(filename, "r+") as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[timestamp] = new_data
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)


if __name__ == "__main__":
    """
    There are now 3 positional arguments

    py ./detector.py path shape timestamp

    We are essentially creating a timestamp key based data structure for the colorOutputs.json.
    This is because if this model and the text classification are to run at the same time,
    how we can get the outputs of both of them to match with one another? What if one finishes before the
    other?

    This may require another script to get the outputs of both models and then finally append them to
    a final shape.

    This model also takes the classified shape and appends it to the json file.

    """

    parser = argparse.ArgumentParser(description="Process an Image file.")
    parser.add_argument(
        "ImagePath", metavar="path", type=str, help="the path to an image file"
    )

    parser.add_argument(
        "Shape", metavar="shape name", type=str, help="the name of the shape"
    )

    parser.add_argument("Timestamp", metavar="time", type=str, help="the current time")

    args = parser.parse_args()

    if args.ImagePath is None:
        print("Please provide the path to an image file.")
        exit()

    if args.Shape is None:
        print("Please provide the name of the shape.")
        exit()

    if args.Timestamp is None:
        print("Please provide the current time.")
        exit()

    image = Image.open(args.ImagePath)

    innerJSON = {"SHAPE": args.Shape}

    width, height = image.size
    left = width * 0.3
    top = height * 0.3
    right = width * 0.7
    bottom = height * 0.7

    # Isolate shape and text
    cropped = image.crop((left, top, right, bottom))

    top_colors = get_dominant_colors(cropped, max_colors=3)
    print(top_colors)
    color_values = [top_colors[i][0] for i in range(len(top_colors))]

    # create list of colors while at the same time appending them to a json file
    color_labels = []

    for i in range(len(top_colors)):
        color = closest_color(top_colors[i][0])
        color_labels.append(f"{color}\n{top_colors[i][1]}")

        if i == 0:
            innerJSON["SHAPE_COLOR"] = color
        elif i == 1:
            innerJSON["TEXT_COLOR"] = color

    write_json(innerJSON, args.Timestamp)

    executionTime = (time.time() - startTime)
    print('\nExecution time in seconds: ' + str(executionTime))

    # Show cropped image
    plt.subplot(1, 2, 1)
    plt.imshow(cropped)
    plt.title("Cropped Image")

    # Show color plot
    plt.subplot(1, 2, 2)
    plt.imshow([color_values])
    plt.xticks(range(len(color_labels)), color_labels)
    plt.title("Dominant Colors")
    plt.show()
