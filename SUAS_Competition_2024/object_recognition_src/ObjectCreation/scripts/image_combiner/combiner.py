from PIL import Image, ImageDraw
import os, random, datetime

BG_PATH = 'E:\\2023\\synthetic_data_collection\\background'
FG_PATH = 'E:\\2023\\synthetic_data_collection\\targetsWithAlphaNum'

def get_scaling(name):
    upper = 0.05
    lower = 0.45

    name = name.split('_')[1]

    match name:
        case "star":
            lower = 0.045
        case "cross":
            lower = 0.0275
        case "pentagon":
            lower = 0.035
        case "triangle":
            lower = 0.035
        case "rectangle":
            lower = 0.0275
        case "quartercircle":
            lower = 0.0275
        case "semicircle":
            lower = 0.02125
        case "circle":
            lower = 0.0225
    return random.uniform(lower, upper)

def add_bounding_box(im, color, margin=5):
    new_im = Image.new('RGBA', (fg_width + 2*margin, fg_height + 2*margin), (0, 0, 0, 0)) 
    new_im.paste(im, (margin, margin))
    w, h = new_im.size

    draw = ImageDraw.Draw(new_im)
    draw.line((0, 0, 0, h), fill=color, width=3)
    draw.line((w, 0, w, h), fill=color, width=3)
    draw.line((0, 0, w, 0), fill=color, width=3)
    draw.line((0, h, w, h), fill=color, width=3)
    return new_im

# run in debugger or cmd or something
for i in range(1):
    # gets random image from random subfolder of base path
    rand_subfolder = os.path.join(BG_PATH, random.choice(os.listdir(BG_PATH)))
    rand_bg = os.path.join(rand_subfolder, random.choice(os.listdir(rand_subfolder)))
    rand_fg = os.path.join(FG_PATH, random.choice(os.listdir(FG_PATH)))

    rand_bg = "E:\\2023\\synthetic_data_collection\\background\\a000\\Video_Breakdown43281.png"
    rand_fg = "E:\\2023\\synthetic_data_collection\\targetsWithAlphaNum\\blue_circle_X_orange.png"
    # skips images whose text is same color as shape color
    img_name = os.path.basename(rand_fg)
    image_name = img_name.split('.')[0]
    image_name = image_name.split('_')
    if image_name[0] == image_name[-1]:
        # print(image_name[0], image_name[-1])
        continue

    # opens the images
    background = Image.open(rand_bg)
    foreground = Image.open(rand_fg)

    # scales down shapes
    # scale_factor = random.uniform(0.025, 0.04)
    scale_factor = get_scaling(os.path.basename(img_name))
    foreground = foreground.resize((int(foreground.size[0] * scale_factor), int(foreground.size[1] * scale_factor)), resample=Image.BILINEAR)

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

    foreground = add_bounding_box(foreground, 'Yellow')

    # creates 12 images, each rotated 30 degrees more than the previous
    for i in range(12):
        rotation = i * 30
        new_bg = background.copy()
        new_fg = foreground.rotate(rotation, expand=True, resample=Image.BICUBIC)
        new_bg.paste(new_fg, coords, new_fg)

        # generates unique image name
        new_filename = rand_fg.split("\\")[-1].split(".")[0] + "_" + rand_bg.split("\\")[-1].split(".")[0]
        new_filename += str(90 * i) + '_' + str(formatted_now) + ".png"
        new_bg.save(f'E:\\2023\\synthetic_data_collection\\combined_images\\{new_filename}', 'PNG')

