import argparse
import configparser
import logging
import os
import subprocess

import cv2
import easyocr
import numpy as np
import torch


class OCRProcessor:
    # Read configuration from constants.config
    config = configparser.ConfigParser()
    config.read("constants.config")

    # Load global variables from config file
    LOCAL_FOLDER_PATH = config["ALPHANUMERIC"]["LOCAL_FOLDER_PATH"]
    ALLOW_LIST = config["ALPHANUMERIC"]["ALLOW_LIST"]
    BLOCK_LIST = config["ALPHANUMERIC"]["BLOCK_LIST"]
    ENABLE_GPU = config.getboolean("ALPHANUMERIC", "GPU")
    OUTPUT_PATH = config["ALPHANUMERIC"]["output_dir"]

    def __init__(self):
        logging.basicConfig(filename="ocr_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)
        self.logger.warning("OUTPUT_PATH has not been set yet.")

        # Initialize OCR reader
        self.ocr_reader = easyocr.Reader(["en"], gpu=self.ENABLE_GPU)

        self.logger.info("Initialized OCRProcessor.")

    def check_local_folder(self, local_folder_path) -> None:
        try:
            if os.path.exists(local_folder_path):
                self.logger.info("Local folder accessible")
            else:
                logging.error(f"Local folder not found: {local_folder_path}")
                raise FileNotFoundError(f"Local folder not found: {local_folder_path}")
        except OSError as e:
            logging.error(f"Error accessing local folder: {local_folder_path}. Exception: {e}")
            raise OSError(f"Error accessing local folder: {local_folder_path}. Exception: {e}")

    def get_device_details(self):
        if torch.cuda.is_available() and self.ENABLE_GPU:
            device_name = torch.cuda.get_device_name()
            logging.info(f"CUDA is available. Using GPU: {device_name}")
            return torch.device("cuda"), device_name
        else:
            logging.info("CUDA is not available. Using CPU.")
            return torch.device("cpu"), "CPU"

    def adjust_contrast_brightness(self, image: np.ndarray, contrast: float = 1.0, brightness: int = 0) -> np.ndarray:
        brightness += int(round(255 * (1 - contrast) / 2))
        return cv2.addWeighted(image, contrast, image, 0, brightness)

    def kmeans_quantization(self, image: np.ndarray, num_colors: int = 5) -> np.ndarray:
        try:
            pixels = image.reshape(-1, 3).astype(np.float32)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 69, 1.0)
            _, labels, colors = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            colors = np.uint8(colors)
            quantized_pixels = colors[labels.flatten()]
            return quantized_pixels.reshape(image.shape)
        except Exception as e:
            logging.error(f"Error performing K-means quantization: {e}")
            raise

    def preprocess_image(self, image_path: str) -> cv2.Mat | np.ndarray:
        self.logger.warning("preprocess_image() type hint/type annotation is assumed and needs to be tested.")
        try:
            image = cv2.imread(image_path)
            blurred_image = cv2.medianBlur(image, 67)
            adjusted_image = self.adjust_contrast_brightness(blurred_image, 3, -100)
            rgb_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)
            quantized_image = self.kmeans_quantization(rgb_image)
            result_image = cv2.bilateralFilter(quantized_image, 9, 75, 75)

            return result_image
        except Exception as e:
            logging.error(f"Error preprocessing image: {e}")
            raise

    def perform_ocr(self, preprocessed_image: np.ndarray):
        try:
            result = self.ocr_reader.readtext(preprocessed_image, detail=1, decoder="beamsearch")
            if result:
                whitelisted_text = "".join([text for text in result[0][1] if text.isalnum()])
                logging.info(f"Detected text: {whitelisted_text}")
                return result
            else:
                logging.info("No text detected.")
                return None
        except Exception as e:
            logging.error(f"Error performing OCR: {e}")
            raise

    def save_results(self, image_path: str, result):
        output_file_path = os.path.join(self.OUTPUT_PATH, os.path.basename(image_path) + ".txt")
        try:
            with open(output_file_path, "w") as file:
                file.write(str(result))
            logging.info(f"Results saved to {output_file_path}")
        except Exception as e:
            logging.error(f"Error saving results: {e}")
            raise

    def main(self, image_path):
        self.check_local_folder(self.LOCAL_FOLDER_PATH)

        device, device_name = self.get_device_details()
        print(f"Using device: {device_name}")

        preprocessed_image = self.preprocess_image(image_path)
        if preprocessed_image is None:
            print("Error preprocessing image. Check logs for details.")
            return

        result = self.perform_ocr(preprocessed_image)
        if result:
            self.save_results("/usr/app/checklist", result)
        else:
            print("No text detected.")

        subprocess.run(["./delete.sh"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess and perform OCR on an image")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    args = parser.parse_args()

    OCR = OCRProcessor()
    OCR.main(args.image_path)
