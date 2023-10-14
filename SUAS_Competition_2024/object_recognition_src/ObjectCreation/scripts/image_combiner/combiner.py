from PIL import Image
import os, random, datetime

BG_PATH = r'C:\Users\joshu\Downloads\s0303\S0303'
FG_PATH = r'C:\Users\joshu\Downloads\targetsWithAlphaNum\targetsWithAlphaNum'

# gets a random image from each of the folders
rand_bg = os.path.join(BG_PATH + '/', random.choice(os.listdir(BG_PATH)))
rand_fg = os.path.join(FG_PATH + '/', random.choice(os.listdir(FG_PATH)))

# opens the images
background = Image.open(rand_bg)
foreground = Image.open(rand_fg)

# scales down shapes
foreground = foreground.resize((int(foreground.size[0] * 0.075), int(foreground.size[1] * 0.075)))

# gets image dimensions
bg_width, bg_height = background.size
fg_width, fg_height = foreground.size

max_x = bg_width - fg_width
max_y = bg_height - fg_height

# gets a random coordinate value that is less than the max
coords = (random.randint(0, max_x), random.randint(0, max_y))


now = datetime.datetime.now()
formatted_now = now.strftime("%f")

for i in range(3):
    new_bg = background.copy()
    new_bg.paste(foreground, coords, foreground)
    # generates unique image name
    new_filename = rand_fg.split("/")[1].split(".")[0] + "_" + rand_bg.split("/")[1].split(".")[0]
    new_filename += str(90 * i) + '_' + str(formatted_now) + ".png"
    new_bg.save(f'output/{new_filename}', 'PNG')
    foreground = foreground.transpose(Image.ROTATE_90)




# closes pointers
foreground.close()
background.close()

