from PIL import Image

image = Image.open(r'C:\Users\joshu\OneDrive\Documents\VsCode\ImageCombiner\foregrounds\fg.png')
image = image.resize((int(image.size[0] * 0.5), int(image.size[1] * 0.5)))
image.show()
image.save(r'C:\Users\joshu\OneDrive\Documents\VsCode\ImageCombiner\foregrounds\fg.png')