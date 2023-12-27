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
    "brown": (150, 75, 0)
    }

def vid2rgb(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = image[y, x]
        colorsRGB = tuple(reversed(colorsBGR))
        color_name = closest_color(colorsRGB, COLORS)
        print(f"At, ({x},{y}), the closest color to RGB value {colorsRGB} is **{color_name}**.")

def closest_color(requested_color, color_dict):
    min_colors = {}
    for color_name, color_rgb in color_dict.items():
        rd = (color_rgb[0] - requested_color[0]) ** 2
        gd = (color_rgb[1] - requested_color[1]) ** 2
        bd = (color_rgb[2] - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = color_name
    return min_colors[min(min_colors.keys())]


image = cv2.imread(r"SUAS_Competition_2024\object_recognition_src\ObjectCreation\testImages\black_pentagon_0_green.png")
cv2.namedWindow('ColorDetection')
cv2.setMouseCallback('ColorDetection', vid2rgb)

while(1):
    cv2.imshow('ColorDetection', image)
    if cv2.waitKey(0):
        break

cv2.destroyAllWindows()
