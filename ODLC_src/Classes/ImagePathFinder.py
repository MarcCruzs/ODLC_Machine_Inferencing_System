import os
import queue
import threading


class ImagePathFinder:
    def __init__(self, captured_images_dir):
        self.captured_images_dir = captured_images_dir
        self.image_path_queue = queue.Queue()
        self.lock = threading.Lock()

    def __call__(self):
        # Ensure the directory exists
        if not os.path.exists(self.captured_images_dir):
            print("Captured images directory doesn't exist.")
            return []

        # Parse through the captured images directory
        for filename in os.listdir(self.captured_images_dir):
            if filename.endswith(".jpg"):
                image_path = os.path.join(self.captured_images_dir, filename)
                self.image_path_queue.put(image_path)
                # Delete the image after extracting its pathway
                os.remove(image_path)

        # Now you have a list of pathways of images
        while not self.image_path_queue.empty():
            image_path = self.image_path_queue.get()
            # Call your YOLOv5 object recognition model here with the image_path


# Example usage
if __name__ == "__main__":
    # Directory containing captured images
    captured_images_dir = "/path_to_captured_images"

    # Create an instance of ImagePathFinder
    image_path_finder = ImagePathFinder(captured_images_dir)

    # Call the instance to find image pathways and process them using YOLOv5
    image_path_finder()
