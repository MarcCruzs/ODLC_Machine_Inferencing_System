import os, re, subprocess, glob
import numpy as np
import torch
from PIL import Image, ImageEnhance
import easyocr
import cv2
from matplotlib import pyplot as plt
import logging
import time
import argparse


startTime = time.time()

logging.basicConfig(filename='ocr_log.log', level=logging.INFO, format='%(asctime)s -  %(levelname)s - %(message)s')

#image loading
local_folder_path = "/raw_images/"
image_path = glob.glob(local_folder_path + "*.jpg")
ocrReader = easyocr.Reader(['en'], gpu=True)
allowlist = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
blocklist = "!@#$%^&*()_~[]\{}|;':,./<>?"
try:
    #local folder path exists?
    if os.path.exists(local_folder_path):
        local_folder_mounted = True
    else:
        local_folder_mounted = False
        raise FileNotFoundError(f"Local folder not found: {local_folder_path}")
except Exception as e:
    local_folder_mounted = False
    logging.error(f"Error checking local folder: {e}")

if local_folder_mounted:
    print("Success!!!", local_folder_path)
    logging.info("Local folder accessed")
else:
    print("Failed to access")
    logging.error("Failed to load local folder")
  

    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name()}")
        logging.info(f"CUDA is available. Using GPU: {torch.cuda.get_device_name()}")
    else:
        device = torch.device("cpu")
        print("CUDA is not available. Using CPU.")
        logging.info("CUDA is not available. Using CPU.")

#use code to call bash script to delete image from /raw_images
subprocess.run(["./delete.sh"])
       

 

    
#mex josh color function lets c if it works
def adjust_contrast_brightness(
    image_path: Image, contrast: float = 1.0, brightness: int = 0
) -> Image:
    """
    Adjusts contrast and brightness of a uint8 image.
    contrast: (0.0, inf) with 1.0 leaving the contrast as is
    brightness: [-255, 255] with 0 leaving the brightness as is
    """
    brightness += int(round(255 * (1 - contrast) / 2))
    return cv2.addWeighted(image_path, contrast, image_path, 0, brightness)

#quantization function, can change arguments for num_colors for desired final amount of colors
def kmeans_quantization(image, num_colors=5):
    try:
        pixels = image.reshape(-1, 3).astype(np.float32)

        #k equation
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 69, 1.0)
        _, labels, colors = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        colors = np.uint8(colors)
        quantized_pixels = colors[labels.flatten()]

        quantized_image = quantized_pixels.reshape(image.shape)

        return quantized_image

    except Exception as e:
        logging.error(f"Error performing K-means quantization: {e}")
        return None

#preprocessing image function
def preprocess_image(image_path):
    try:
        #mex josh
        testing_image = cv2.imread(image_path, 1)
        gaussian_blur =  cv2.medianBlur(testing_image, 67)
        t_image = adjust_contrast_brightness(gaussian_blur, 3, -100)

        rgb_image = cv2.cvtColor(t_image, cv2.COLOR_BGR2RGB)
        quantized_image = kmeans_quantization(rgb_image)
        quantized_image = cv2.bilateralFilter(quantized_image, 9, 75, 75)

        return quantized_image

    except Exception as e:
        logging.error(f"Error preprocessing image: {e}")
        return None

preprocessed_image = preprocess_image(image_path)
# display(preprocessed_image, title="preprocessed image")


try:
    result = ocrReader.readtext(preprocessed_image, detail=0, decoder='beamsearch')
    print(result)
    if result:
        whitelisted_text = ''.join([text for text in result[0] if text.isalnum()])
        print("Whitelisted text:", whitelisted_text)
        
        top_left = tuple(result[0][0][0])
        bottom_right = tuple(result[0][0][2])
        text = result[0][1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        #floating point fix but str obj? fixed
        print("Top left:", top_left)
        print("Bottom right:", bottom_right)
        top_left = (int(top_left[0]), int(top_left[1]))
        bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
        print("Top left:", top_left)
        print("Bottom right:", bottom_right)


        image2 = cv2.imread(image_path)
        image2 = cv2.rectangle(image2, top_left, bottom_right, (0, 255, 0), 5)
        image2 = cv2.putText(image2, text, top_left, font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        plt.imshow(image2)
        plt.show()
    else:
        print("No text detected.")
        logging.info("No text detected.")

except Exception as e:
    logging.error(f"Error performing OCR: {e}")
    print("Error performing OCR. Check logs for details.")
    
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess and perform OCR on an image")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args