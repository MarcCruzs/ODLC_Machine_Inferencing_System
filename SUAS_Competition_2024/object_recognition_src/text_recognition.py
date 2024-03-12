import os
import numpy as np
import torch
from PIL import Image, ImageEnhance
import easyocr
import cv2
from matplotlib import pyplot as plt
import logging
import time
import tempfile

startTime = time.time()

logging.basicConfig(filename='ocr_log.log', level=logging.INFO, format='%(asctime)s -  %(levelname)s - %(message)s')

#image loading
local_folder_path = "E:\\SUAS\\targetsWithAlphaNum"
image_path = "E:\\SUAS\\testImages\\green_trapeziod_8_yellow.jpg"

ocrReader = easyocr.Reader(['en'], gpu=True)

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
  
try:
    image = Image.open(image_path)
    image_np = np.array(image)
    plt.imshow(image)
    plt.axis('off')
    plt.show()
except Exception as e:
    logging.error(f"Error opening image: {e}")
    exit()

    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name()}")
        logging.info(f"CUDA is available. Using GPU: {torch.cuda.get_device_name()}")
    else:
        device = torch.device("cpu")
        print("CUDA is not available. Using CPU.")
        logging.info("CUDA is not available. Using CPU.")
 
        
 #display functions
def display(image, title='Image'):
    plt.title(title)
    plt.axis('off')
    plt.imshow(image)
    plt.show()
    
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
       
#preprocessing image stuff may/maynot need

#image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
#display(image_cv, title='BGR')

#gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)  
# display(gray_image, title='gray')

#_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY) 
#display(binary_image, title='binary image')

#image_opening = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN,kernel2)
#display(image_opening, title='open')

# image_dilation = cv2.dilate(image_opening, kernel, iterations=1)
#display(image_dilation, title='dilated image')

#denoised_image = cv2.fastNlMeansDenoising(binary_image, None, 10, 10, 7, 15)  
#display(denoised_image, title='denoised image')

#gaussian_blur = cv2.GaussianBlur(image_cv, (33,33), 0)
#display(gaussian_blur, title='gaussian blur image')

# median_blur = cv2.medianBlur(denoised_image, 7)
#display(median_blur, title='median blur')

#avg_blur=cv2.blur(denoised_image, (15,15))
#display(avg_blur, title='avg blur')

#bilateral_blur = cv2.bilateralFilter(gaussian_blur, 15, 75, 75)
#display(bilateral_blur, title='bilateral blur image')

def kmeans_quantization(image, num_colors=8):
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


#image process function no longer for roi for post quantizing    

def preprocess_image(image_path):
    try:
        #mex josh
        testing_image = cv2.imread(image_path, 1)
        testing_image = adjust_contrast_brightness(testing_image, 3, -120)

        rgb_image = cv2.cvtColor(testing_image, cv2.COLOR_BGR2RGB)
        quantized_image = kmeans_quantization(rgb_image)

        return quantized_image

    except Exception as e:
        logging.error(f"Error preprocessing image: {e}")
        return None
    

preprocessed_image = preprocess_image(image_path)
display(preprocessed_image, title="pp image")

with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image_file:
    temp_image_filename = temp_image_file.name
    cv2.imwrite(temp_image_filename, preprocessed_image)


try:
    result = ocrReader.readtext(preprocessed_image)
    print(result)
    if result:
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
