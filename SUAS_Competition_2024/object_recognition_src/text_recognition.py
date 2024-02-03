# text_recognition.py
# The purpose of this script is to use easyOCR to detect texts
# Author/s: Josh Ng, Marc Cruz
import os
import numpy as np
import torch
from PIL import Image
import easyocr
import cv2
from matplotlib import pyplot as plt

# pathway to a folder containing various images
FOLDER_PATH = "/test_cases/"

# Try/catch is checking for folder path is valid
try:
    if os.path.exists(FOLDER_PATH):
        print("Success!!!", FOLDER_PATH)
    else:
        print("Failed to access")
except Exception as e:
    local_folder_mounted = False
    print(f"Error checking local folder: {e}")

# Relative path to a specific image to test with
IMAGE_PATH = "test_cases/BLURRED_yellow_triangle_green_L.jpg"

# Checking if image exists
try:
    image = Image.open(IMAGE_PATH)
except Exception as e:
    print(f"Error opening image: {e}")
    exit()

# Testing for CUDA compatitable GPU
# if torch.cuda.is_available():
#     device = torch.device("cuda")
#     print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name()}")
# else:
#     print("CUDA is not available. Using CPU.")

# easyOCR Implementation to detect alphanumeric
try:
    ocrReader = easyocr.Reader(['en'], gpu=True)
    result = ocrReader.readtext(IMAGE_PATH)
    print(result)

    if result:
        top_left = tuple(result[0][0][0])
        bottom_right = tuple(result[0][0][0])
        text = result[0][1]
        font = cv2.FONT_HERSHEY_SIMPLEX

        image2 = cv2.imread(IMAGE_PATH)
        image2 = cv2.rectangle(image2, top_left, bottom_right, (0, 255, 0), 5)
        image2 = cv2.putText(image2, text, top_left, font, 1, (255, 255, 2555), 2, cv2.LINE_AA)

except Exception as e:
    print(f"Error performing OCR: {e}")
