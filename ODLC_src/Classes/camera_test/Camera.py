import cv2
import os
import uuid
import argparse

class Camera:
    def __init__(self, camera_device):
        self.camera_device = camera_device
        self.cap = cv2.VideoCapture(self.camera_device)
        print(f"Trying to open camera device {self.camera_device}...")

        if not self.cap.isOpened():
            raise ValueError(f"Unable to open camera device {self.camera_device}")
        else:
            print(f"Successfully opened camera device {self.camera_device}")

    def take_picture(self):
        print("Attempting to capture image...")
        ret, frame = self.cap.read()

        if not ret:
            raise ValueError("Failed to capture image from camera")

        print("Image captured successfully.")
        return frame

    def save_to_folders(self, image, folder1, folder2):
        filename = str(uuid.uuid4()) + ".jpg"
        
        if not os.path.exists(folder1):
            os.makedirs(folder1)
        if not os.path.exists(folder2):
            os.makedirs(folder2)

        file_path1 = os.path.join(folder1, filename)
        file_path2 = os.path.join(folder2, filename)

        print(f"Saving image to {file_path1} and {file_path2}...")
        cv2.imwrite(file_path1, image)
        cv2.imwrite(file_path2, image)
        print("Image saved successfully.")

    def release(self):
        print("Releasing camera...")
        self.cap.release()
        print("Camera released.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process camera device and folder paths')
    parser.add_argument('--camera_device', type=int, default=int(os.getenv('CAMERA_DEVICE', 0)), help='Camera device index (e.g., 0, 1, 2) for windows. Camera pathway (i.g. /dev/video0) for linux.')
    parser.add_argument('--folder1', default='./Folder1', help='Path to folder1')
    parser.add_argument('--folder2', default='./Folder2', help='Path to folder2')
    args = parser.parse_args()

    try:
        camera = Camera(args.camera_device)
        image = camera.take_picture()
        camera.save_to_folders(image, folder1=args.folder1, folder2=args.folder2)
    except ValueError as e:
        print(f"Error: {e}")
    finally:
        camera.release()
