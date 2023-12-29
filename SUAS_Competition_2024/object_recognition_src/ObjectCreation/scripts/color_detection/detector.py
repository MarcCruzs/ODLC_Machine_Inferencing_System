from PIL import Image
import cv2

# use pre-defined rgb values for SUAS-specified colors
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "purple": (128, 0, 128),
    "white": (255, 255, 255),
    "orange": (255, 165, 0),
    "brown": (150, 75, 0),
}


# def get_dominant_colors(pil_img, palette_size=16, num_colors=4):
#     # Resize image to speed up processing
#     img = pil_img.copy()
#     img.thumbnail((100, 100))

#     # Reduce colors (uses k-means internally)
#     paletted = img.convert("P", palette=Image.ADAPTIVE, colors=palette_size)

#     # Find the color that occurs most often
#     palette = paletted.getpalette()
#     color_counts = sorted(paletted.getcolors(), reverse=True)

#     total_pixels = img.size[0] * img.size[1]
#     dominant_colors = []
#     for i in range(num_colors):
#         palette_index = color_counts[i][1]
#         color_count = color_counts[i][0]
#         color_percentage = (color_count / total_pixels) * 100
#         dominant_colors.append(
#             {
#                 "color": palette[palette_index * 3 : palette_index * 3 + 3],
#                 "percentage": color_percentage,
#             }
#         )

#     return dominant_colors


def get_dominant_colors(pil_img, palette_size=16, max_colors=6):
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
        color_percentage = color_count / total_pixels
        color = palette[palette_index * 3 : palette_index * 3 + 3]
        if color not in [c[0] for c in dominant_colors]:  # Skip adding duplicate colors
            dominant_colors.append((color, color_percentage))

    return dominant_colors


def vid2rgb(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = image[y, x]
        colorsRGB = tuple(reversed(colorsBGR))
        color_name = closest_color(colorsRGB, COLORS)
        print(
            f"At, ({x},{y}), the closest color to RGB value {colorsRGB} is **{color_name}**."
        )


def closest_color(requested_color):
    min_colors = {}
    for color_name, color_rgb in COLORS.items():
        rd = (color_rgb[0] - requested_color[0]) ** 2
        gd = (color_rgb[1] - requested_color[1]) ** 2
        bd = (color_rgb[2] - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = color_name
    return min_colors[min(min_colors.keys())]


if __name__ == "__main__":
    image = Image.open(
        r"SUAS_Competition_2024\object_recognition_src\ObjectCreation\testImages\blue_pentagon_M_purple.png"
    )
    top_colors = get_dominant_colors(image)
    print(top_colors)
    for top_color, dominance in top_colors:
        if dominance < 0.01:
            continue
        if dominance > 0.5:
            print("Shape color:", closest_color(top_color))
        else:
            print("Text color:", closest_color(top_color))

    # cv2.namedWindow("ColorDetection")
    # cv2.setMouseCallback("ColorDetection", vid2rgb)

    # while 1:
    #     cv2.imshow("ColorDetection", image)
    #     if cv2.waitKey(0):
    #         break

    # cv2.destroyAllWindows()
