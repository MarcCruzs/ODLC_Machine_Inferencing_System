import os
import numpy as np
import torch
from PIL import Image
import easyocr
import cv2
from matplotlib import pyplot as plt

# download external data set of shapes/colors/text
local_folder_path = "E:\\SUAS\\targetsWithAlphaNum"

try:
    # Check if the local folder path exists
    if os.path.exists(local_folder_path):
        local_folder_mounted = True
    else:
        local_folder_mounted = False
except Exception as e:
    local_folder_mounted = False
    print(f"Error checking local folder: {e}")

if local_folder_mounted:
    print("Success!!!", local_folder_path)
else:
    print("Failed to access")

# image preprocessing
image_path = "E:\\SUAS\\targetsWithAlphaNum/black_pentagon_2_brown.png"

try:
    image = Image.open(image_path)
    plt.imshow(image)
    plt.axis("on")
    plt.show()
except Exception as e:
    print(f"Error opening image: {e}")
    exit()

if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name()}")
else:
    print("CUDA is not available. Using CPU.")


try:
    ocrReader = easyocr.Reader(["en"], gpu=True)
    result = ocrReader.readtext(image_path)
    print(result)

    if result:
        top_left = tuple(result[0][0][0])
        bottom_right = tuple(result[0][0][0])
        text = result[0][1]
        font = cv2.FONT_HERSHEY_SIMPLEX

        image2 = cv2.imread(image_path)
        image2 = cv2.rectangle(image2, top_left, bottom_right, (0, 255, 0), 5)
        image2 = cv2.putText(
            image2, text, top_left, font, 1, (255, 255, 2555), 2, cv2.LINE_AA
        )
        plt.imshow(image2)
        plt.show()

except Exception as e:
    print(f"Error performing OCR: {e}")
