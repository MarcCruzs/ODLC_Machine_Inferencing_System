from PIL import Image
from matplotlib import pyplot as plt
import argparse

# use pre-defined rgb values for SUAS-specified colors
COLORS = {
    "red": (128, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 128),
    "black": (0, 0, 0),
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process an Image file.")
    parser.add_argument(
        "ImagePath", metavar="path", type=str, help="the path to an image file"
    )

    args = parser.parse_args()
    if args.ImagePath is None:
        print("Please provide the path to an image file.")
        exit()

    image = Image.open(args.ImagePath)

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
    color_labels = [
        f"{closest_color(top_colors[i][0])}\n{top_colors[i][1]}"
        for i in range(len(top_colors))
    ]

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
