import os
import subprocess
import glob
import numpy as np
import torch
from PIL import Image
import easyocr
import cv2
from matplotlib import pyplot as plt
import logging
import time
import argparse
import configparser

# Initialize start time and logging
startTime = time.time()
logging.basicConfig(filename='ocr_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read configuration from constants.config
config = configparser.ConfigParser()
config.read('constants.config')

# Load global variables from config file
local_folder_path = config['ALPHANUMERIC']['LOCAL_FOLDER_PATH']
allowlist = config['ALPHANUMERIC']['ALLOW_LIST']
blocklist = config['ALPHANUMERIC']['BLOCK_LIST']
use_gpu = config.getboolean('ALPHANUMERIC', 'GPU')
output_dir = config['ALPHANUMERIC']['output_dir']

# Initialize OCR reader
ocrReader = easyocr.Reader(['en'], gpu=use_gpu)

def check_local_folder(local_folder_path):
    try:
        if os.path.exists(local_folder_path):
            logging.info("Local folder accessed")
            return True
        else:
            raise FileNotFoundError(f"Local folder not found: {local_folder_path}")
    except Exception as e:
        logging.error(f"Error checking local folder: {e}")
        return False

def get_device():
    if torch.cuda.is_available() and use_gpu:
        device_name = torch.cuda.get_device_name()
        logging.info(f"CUDA is available. Using GPU: {device_name}")
        return torch.device("cuda"), device_name
    else:
        logging.info("CUDA is not available. Using CPU.")
        return torch.device("cpu"), "CPU"

def adjust_contrast_brightness(image: np.ndarray, contrast: float = 1.0, brightness: int = 0) -> np.ndarray:
    brightness += int(round(255 * (1 - contrast) / 2))
    return cv2.addWeighted(image, contrast, image, 0, brightness)

def kmeans_quantization(image: np.ndarray, num_colors: int = 5) -> np.ndarray:
    try:
        pixels = image.reshape(-1, 3).astype(np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 69, 1.0)
        _, labels, colors = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        colors = np.uint8(colors)
        quantized_pixels = colors[labels.flatten()]
        return quantized_pixels.reshape(image.shape)
    except Exception as e:
        logging.error(f"Error performing K-means quantization: {e}")
        return None

def preprocess_image(image_path: str) -> np.ndarray:
    try:
        image = cv2.imread(image_path)
        blurred_image = cv2.medianBlur(image, 67)
        adjusted_image = adjust_contrast_brightness(blurred_image, 3, -100)
        rgb_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)
        quantized_image = kmeans_quantization(rgb_image)
        return cv2.bilateralFilter(quantized_image, 9, 75, 75)
    except Exception as e:
        logging.error(f"Error preprocessing image: {e}")
        return None

def perform_ocr(preprocessed_image: np.ndarray):
    try:
        result = ocrReader.readtext(preprocessed_image, detail=1, decoder='beamsearch')
        if result:
            whitelisted_text = ''.join([text for text in result[0][1] if text.isalnum()])
            logging.info(f"Detected text: {whitelisted_text}")
            return result
        else:
            logging.info("No text detected.")
            return None
    except Exception as e:
        logging.error(f"Error performing OCR: {e}")
        return None

def save_results(image_path: str, result):
    output_file_path = os.path.join(output_dir, os.path.basename(image_path) + '.txt')
    try:
        with open(output_file_path, 'w') as file:
            file.write(str(result))
        logging.info(f"Results saved to {output_file_path}")
    except Exception as e:
        logging.error(f"Error saving results: {e}")

def main(image_path):
    if not check_local_folder(local_folder_path):
        logging.error("Failed to load local folder")
        return

    device, device_name = get_device()
    print(f"Using device: {device_name}")

    preprocessed_image = preprocess_image(image_path)
    if preprocessed_image is None:
        print("Error preprocessing image. Check logs for details.")
        return

    result = perform_ocr(preprocessed_image)
    if result:
        save_results("/usr/app/checklist", result) #######
    else:
        print("No text detected.")

    subprocess.run(["./delete.sh"])


    executionTime = (time.time() - startTime)
    print(f'Execution time in seconds: {executionTime}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess and perform OCR on an image")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args()
    main(args.image_path)
