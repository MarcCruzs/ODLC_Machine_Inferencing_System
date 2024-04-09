import cv2
import os
import uuid
import argparse  # Import argparse module for command-line argument parsing

class Camera:
    def __init__(self, camera_device):
        self.camera_device = camera_device
        self.cap = cv2.VideoCapture(self.camera_device)
        
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open camera device {self.camera_device}")

    def take_picture(self):
        ret, frame = self.cap.read()

        if not ret:
            raise ValueError("Failed to capture image from camera")

        return frame

    def save_to_folders(self, image, folder1, folder2):
        filename = str(uuid.uuid4()) + ".jpg"
        
        file_path1 = os.path.join(folder1, filename)
        file_path2 = os.path.join(folder2, filename)

        cv2.imwrite(file_path1, image)
        cv2.imwrite(file_path2, image)

    def release(self):
        self.cap.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process camera device and folder paths')
    parser.add_argument('camera_device', help='Path to the camera device (e.g., /dev/video0)')
    parser.add_argument('--folder1', default='./Folder1', help='Path to folder1')
    parser.add_argument('--folder2', default='./Folder2', help='Path to folder2')
    args = parser.parse_args()

    camera = Camera(args.camera_device)

    image = camera.take_picture()

    camera.save_to_folders(image, folder1=args.folder1, folder2=args.folder2)

    camera.release()
