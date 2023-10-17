from PIL import Image, ImageDraw
import os, random, datetime

BG_PATH = r'C:\Users\joshu\Downloads\s0303\S0303'
FG_PATH = r'E:\targetsWithAlphaNum'

while True:

    # gets a random image from each of the folders
    rand_bg = os.path.join(BG_PATH + '/', random.choice(os.listdir(BG_PATH)))
    rand_fg = os.path.join(FG_PATH + '/', random.choice(os.listdir(FG_PATH)))

    # skips images whose text is same color as shape color
    image_name = os.path.basename(rand_fg)
    image_name = image_name.split('.')[0]
    image_name = image_name.split('_')
    if image_name[0] == image_name[-1]:
        print(image_name[0], image_name[-1])
        continue
    # opens the images
    background = Image.open(rand_bg)
    foreground = Image.open(rand_fg)

    # scales down shapes
    scale_factor = random.uniform(0.035, 0.10) # Range of 3.5% to 10% scaling
    foreground = foreground.resize((int(foreground.size[0] * scale_factor), int(foreground.size[1] * scale_factor)))

    # gets image dimensions
    bg_width, bg_height = background.size
    fg_width, fg_height = foreground.size

    max_x = bg_width - fg_width
    max_y = bg_height - fg_height

    # gets a random coordinate value that is less than the max
    coords = (random.randint(0, max_x), random.randint(0, max_y))


    now = datetime.datetime.now()
    formatted_now = now.strftime("%f")


    rect_shape =  (0, 0, fg_width + 10, fg_height + 10)
    img = Image.new("RGBA", (fg_width + 10, fg_height + 10), (0,0,0,0))
    rect = ImageDraw.Draw(img)
    rect.rectangle(rect_shape, outline="yellow", width=3)
    rect_coords = (coords[0] - 5, coords[1] - 5)

    for i in range(3):
        new_bg = background.copy()
        new_bg.paste(foreground, coords, foreground)
        new_bg.paste(img, rect_coords, img)

        # generates unique image name
        new_filename = rand_fg.split("/")[1].split(".")[0] + "_" + rand_bg.split("/")[1].split(".")[0]
        new_filename += str(90 * i) + '_' + str(formatted_now) + ".png"
        new_bg.save(f'E:\CombinedImages/{new_filename}', 'PNG')
        foreground = foreground.transpose(Image.ROTATE_90)
        img = img.transpose(Image.ROTATE_90)




    # closes pointers
    foreground.close()
    background.close()

