from PIL import Image

# Load the original image
img = Image.open(r"C:\Users\joshu\Downloads\IMG_4612.jpg")

if img.mode != "RGB":
    img = img.convert("RGB")

pal = {
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 128),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "purple": (128, 0, 128),
    "orange": (255, 165, 0),
    "brown": (150, 75, 0),
    "silver": (169, 169, 169),
}
# Define your custom palette
palette = [item for sublist in pal.values() for item in sublist]

# Create a new image with the custom palette
p_img = Image.new("P", img.size)
p_img.putpalette(palette)

# Quantize the original image using the custom palette
quantized_img = img.quantize(colors=len(palette), palette=p_img, dither=0)

# Show the resulting image
quantized_img.save("testimg2.png")
