# Imports PIL module
import PIL
from PIL import Image, ImageDraw
import os
from itertools import product
import string


shapes = [
    "circle",
    "semicircle",
    "topLeftQuarter circle",
    "topRightQuarter circle",
    "bottomLeftQuarter circle",
    "bottomRightQuarter circle",
    "triangle",
    "rectangle",
    "pentagon",
    "star",
    "cross",
]

colors = ["white", "black", "red", "blue", "green", "purple", "brown", "orange"]
numbers = list(range(1, 10))
alphabet = list(string.ascii_uppercase)

possibleCombs = list(product(shapes,colors,numbers)) + list(product(shapes,colors,alphabet))

for i in range(3080):
    print(possibleCombs[i]) 
print(len(possibleCombs))