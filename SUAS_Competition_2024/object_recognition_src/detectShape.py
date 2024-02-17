import torch
import cv2
from pathlib import Path
from PIL import Image

def detect_objects(image_path):
    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

    # Perform inference
    if str(image_path) == '0':  # If the input is '0', indicating live view
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            results = model(frame)
            cv2.imshow('YOLOv5 Object Detection', results.render()[0])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        image = Image.open(image_path)
        results = model(image)
        # Print detected objects
        print(results.pandas().xyxy[0])  # Access detected objects in a tabular format

if __name__ == "__main__":
    image_path = input("Enter the location of the image or video (0 for live view): ")
    image_path = Path(image_path)
    detect_objects(image_path)