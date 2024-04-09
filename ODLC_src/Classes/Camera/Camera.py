import cv2
import os
import uuid  # Import uuid module to generate unique filenames

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened():
            raise ValueError(f"Unable to open camera with index {self.camera_index}")

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
    # Read folder paths from environment variables or use default values
    folder1 = os.getenv("FOLDER1", "./Folder1")
    folder2 = os.getenv("FOLDER2", "./Folder2")

    camera = Camera()

    image = camera.take_picture()

    camera.save_to_folders(image, folder1=folder1, folder2=folder2)

    camera.release()
