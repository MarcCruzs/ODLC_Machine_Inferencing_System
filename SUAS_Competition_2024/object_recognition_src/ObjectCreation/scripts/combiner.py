from PIL import Image
import os, random, datetime

# run it through command line and just ctrl+c when done
while True:


    # gets a random image from each of the folders
    rand_bg = os.path.join('backgrounds/', random.choice(os.listdir("backgrounds")))
    rand_fg = os.path.join('foregrounds/', random.choice(os.listdir("foregrounds")))

    # opens the images
    background = Image.open(rand_bg)
    foreground = Image.open(rand_fg)

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

