from PIL import Image, ImageDraw
import os, random, datetime

BG_PATH = 'E:\\dataset_backgrounds\\UAV-benchmark-M'
FG_PATH = 'E:\\targetsWithAlphaNum'

# run in debugger or cmd or something
while True:
    # gets random image from random subfolder of base path
    rand_subfolder = os.path.join(BG_PATH, random.choice(os.listdir(BG_PATH)))
    rand_bg = os.path.join(rand_subfolder, random.choice(os.listdir(rand_subfolder)))
    rand_fg = os.path.join(FG_PATH, random.choice(os.listdir(FG_PATH)))

    # skips images whose text is same color as shape color
    image_name = os.path.basename(rand_fg)
    image_name = image_name.split('.')[0]
    image_name = image_name.split('_')
    if image_name[0] == image_name[-1]:
        # print(image_name[0], image_name[-1])
        continue

    # opens the images
    background = Image.open(rand_bg)
    foreground = Image.open(rand_fg)

    # scales down shapes
    scale_factor = random.uniform(0.015, 0.03) # Range of 1.5% to 3% scaling
    foreground = foreground.resize((int(foreground.size[0] * scale_factor), int(foreground.size[1] * scale_factor)))

    # gets image dimensions
    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size

    # sets boundaries to prevent image from going outside the view
    max_x = bg_width - (fg_width + 3)
    max_y = bg_height - (fg_height + 3)

    # gets a random coordinate value that is less than the max
    coords = (random.randint(0, max_x), random.randint(0, max_y))


    now = datetime.datetime.now()
    formatted_now = now.strftime("%f")


    # bounding box code

    # creates outline
    # rect_shape =  (0, 0, fg_width + 10, fg_height + 10)
    # img = Image.new("RGBA", (fg_width + 10, fg_height + 10), (0,0,0,0))
    # rect = ImageDraw.Draw(img)
    # rect.rectangle(rect_shape, outline="yellow", width=3)
    # rect_coords = (coords[0] - 5, coords[1] - 5)

    # foreground.paste(img, (0,0), img)

    # creates 12 images, each rotated 30 degrees more than the previous
    for i in range(12):
        rotation = i * 30
        new_bg = background.copy()
        new_fg = foreground.rotate(rotation, center=(foreground.size[0] / 2, foreground.size[1] / 2), expand=True)
        new_bg.paste(new_fg, coords, new_fg)

        # generates unique image name
        new_filename = rand_fg.split("\\")[-1].split(".")[0] + "_" + rand_bg.split("\\")[-1].split(".")[0]
        new_filename += str(90 * i) + '_' + str(formatted_now) + ".png"
        new_bg.save(f'E:/CombinedImages/{new_filename}', 'PNG')

