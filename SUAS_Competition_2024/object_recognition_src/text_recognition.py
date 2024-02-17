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
image_path = "E:\\SUAS\\testImages\\ZOOMED_green_hexagon_white_i.jpg"

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
    

    dominant_colors = get_dominant_colors(image)
    
    if dominant_colors:
        print("Dominant colors:")
        for count, color in dominant_colors:
            print(f"Color: {color}, Count: {count}")
    else:
        print("No dominant colors found.")
        
 #display functions
def display(image, title='Image'):
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()
def display_roi(roi_file_path, title='ROI Image'):
    roi_image = cv2.imread(roi_file_path)
    plt.imshow(cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()
       
#preprocessing image stuff

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


#image process function
def preprocess_image(image_path):
    try:
        kernel =np.ones((33,33), np.uint8)
        kernel2 =np.ones((11,11), np.float32)/25
        
        image_cv =cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) 
        #image_cv=cv2.imread(image_path)
        gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(gray_image, (123,123), 0)
        _, binary_image = cv2.threshold(gaussian_blur, 150, 255, cv2.THRESH_BINARY) 
        image_opening = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN,kernel2)
        image_dilation = cv2.dilate(image_opening, kernel, iterations=1)

        return image_dilation
    
    except Exception as e:
        logging.error(f"Error preprocessing image: {e}") 

#get dom colors
def get_dominant_colors(image_path, palette_size = 16, max_colors=6):
    try:
         image=Image.open(image_path)
         image.thumbnail((200,200))
         paletted = image.convert("P", palette=Image.ADAPTIVE, colors=palette_size)
         color_counts=paletted.getcolors()
         sorted_colors = sorted(color_counts, key=lambda x: x[0], reverse=True)
         dominant_colors = sorted_colors[:max_colors]
         return dominant_colors
    
    except Exception as e:
        logging.error(f"Error getting dominant colors: {e}") 
def tempSave_roi(roi):
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=True)
    temp_file.close()
    cv2.imwrite(temp_file.name, roi)
    
    return temp_file.name

        
result = get_dominant_colors(image_path)
print(result)
preprocessed_image = preprocess_image(image_path)
display(preprocessed_image, title='image')        

#bounding box function
def bounding_box(preprocessed_image):
    try:
        image = cv2.imread(preprocessed_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter out small contours
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]  # Adjust threshold as needed
        
        contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if h >200 and w >20:
                roi = image[y:y+h, x:x+h]
                cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)
                roi_file_path = tempSave_roi(roi)
        return roi_file_path
    except Exception as e:
        logging.error(f"Error making bounding box: {e}")

#display roi here
roi_temp_file = bounding_box(image_path)
display_roi(roi_temp_file, title="ROI Image")
roi_image = cv2.imread(roi_temp_file)
display(roi_image, title='hehe')

def ppimage(roi_temp_file):
    try:
        kernel =np.ones((5,5), np.uint8)
        kernel2 =np.ones((11,11), np.float32)/25
        
        #image_cv =cv2.cvtColor(np.array(roi_image), cv2.COLOR_RGB2BGR) 
        image=cv2.imread(roi_temp_file)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gaussian_blur = cv2.GaussianBlur(gray_image, (7,7), 0)
        #_, binary_image = cv2.threshold(gaussian_blur, 150, 255, cv2.THRESH_BINARY) 
        #image_opening = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN,kernel2)
        #enhancer = ImageEnhance.Color(roi_image)
        #image = enhancer.enhance(0.0)
        final = cv2.dilate(gaussian_blur, kernel, iterations=1)

        return final
    
    except Exception as e:
        logging.error(f"Error preprocessing image: {e}") 

final_image = ppimage(roi_temp_file)
display(final_image, title='final')

try:
    result = ocrReader.readtext(final_image)
    print(result)
    if result:
        top_left = tuple(result[0][0][0])
        bottom_right = tuple(result[0][0][2])
        text = result[0][1]
        font = cv2.FONT_HERSHEY_SIMPLEX

        image2 = cv2.imread(image)
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
