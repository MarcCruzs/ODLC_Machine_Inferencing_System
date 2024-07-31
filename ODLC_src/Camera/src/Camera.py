import argparse
import logging
import os
import uuid

import cv2
import numpy as np


class Camera:
    logging.basicConfig(
        filename="camera.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - $(funcName)s -  %(message)s",
    )

    def __init__(self, camera_device):
        self.logger = logging.getLogger(__name__)

        self.logger.warning("Camera Implementation may need its own docker test suite.")

        self.camera_device = camera_device
        self.cap = cv2.VideoCapture(self.camera_device)
        self.logger.info(f"Trying to open camera device {self.camera_device}")

        if not self.cap.isOpened():
            raise ValueError(f"Unable to open camera device {self.camera_device}")
        else:
            self.logger.info(f"Successfully opened camera device {self.camera_device}")

    def take_picture(self):
        print("Attempting to capture image...")
        ret, frame = self.cap.read()

        if not ret:
            raise ValueError("Failed to capture image from camera")

        self.logger.info("Image captured successfully.")
        return frame

    def save_to_folders(self, image: np.ndarray, raw_folder: str, archive_folder: str) -> None:
        filename = str(uuid.uuid4()) + ".jpg"

        if not os.path.exists(raw_folder):
            os.makedirs(raw_folder)
        if not os.path.exists(archive_folder):
            os.makedirs(archive_folder)

        file_path1 = os.path.join(raw_folder, filename)
        file_path2 = os.path.join(archive_folder, filename)

        self.logger.info(f"Saving image to {file_path1} and {file_path2}")

        cv2.imwrite(file_path1, image)
        cv2.imwrite(file_path2, image)

        self.logger.info("Image saved successfully.")

    def release(self):
        self.logger.info("Releasing camera...")
        self.cap.release()
        self.logger.info("Camera released.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process camera device and folder paths")
    parser.add_argument(
        "--camera_device",
        type=int,
        default=int(os.getenv("CAMERA_DEVICE", 0)),
        help="Camera device index (e.g., 0, 1, 2) for windows. Camera pathway (i.g. /dev/video0) for linux.",
    )
    parser.add_argument("--raw_folder", default="./raw_images", help="Path to raw_images")
    parser.add_argument("--archive_folder", default="./archived_images", help="Path to archived_images")
    args = parser.parse_args()

    camera = Camera(args.camera_device)
    try:
        image = camera.take_picture()
        camera.save_to_folders(image, raw_folder=args.raw_folder, archive_folder=args.archive_folder)
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        camera.release()
