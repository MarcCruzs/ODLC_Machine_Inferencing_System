import cv2
import os

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

    def save_to_folders(self, image, filename, folder1, folder2):
        if not os.path.exists(folder1):
            os.makedirs(folder1)
        if not os.path.exists(folder2):
            os.makedirs(folder2)

        file_path1 = os.path.join(folder1, filename)
        file_path2 = os.path.join(folder2, filename)

        # Save to folder 1
        cv2.imwrite(file_path1, image)
        print(f"Image saved to {file_path1}")

        # Save to folder 2
        cv2.imwrite(file_path2, image)
        print(f"Image saved to {file_path2}")

    def release(self):
        # Release the camera
        self.cap.release()
        print("Camera released")

if __name__ == "__main__":
    # Instantiate the Camera object
    camera = Camera()

    # Take a picture
    image = camera.take_picture()

    # Save the picture to folders
    camera.save_to_folders(image, filename='captured_image.jpg', folder1='folder1', folder2='folder2')

    # Release the camera
    camera.release()
