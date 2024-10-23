import torch
from pathlib import Path
from PIL import Image
import os

def detect_objects(path=None, image_dir=False, conf_threshold=0.25, save_dir=r"C:\Users\syedz\Desktop\CS4610_20\cropped_images"):
    weights_path = r"C:\Users\syedz\Desktop\CS4610_20\ODLC_Machine_Inferencing_System\SUAS_Competition_2024\object_recognition_src\yolov5-master\runs\train\exp19\weights\best.pt"
    # Load your custom-trained YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weights_path)

    # Set confidence threshold
    model.conf = conf_threshold

    # Perform inference
    if str(path) == '0':  # If the input is '0', indicating live view
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
        # Create save directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        if image_dir:
            foldername = os.path.basename(path)
            folder_save_dir = os.path.join(save_dir, f"{foldername}_cropped_images")
            os.makedirs(folder_save_dir, exist_ok=True)

            # Iterate over files in the folder
            for filename in os.listdir(path):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):  # Check if file is an image
                    image_path = os.path.join(path, filename)
                    image = Image.open(image_path)
                    results = model(image)
                    filename_no_ext, ext = os.path.splitext(filename)
                    
                    # Process detected objects
                    for i, obj in enumerate(results.xyxy[0]):
                        x1, y1, x2, y2, conf, class_id = obj.tolist()

                        # Extract coordinates and crop image
                        cropped_image = image.crop((x1, y1, x2, y2))

                        # Save cropped image with appropriate filename
                        cropped_image_path = os.path.join(folder_save_dir, f"{filename_no_ext}_cropped_{i}{ext}")
                        cropped_image.save(cropped_image_path)

                        # Print bounding box coordinates and cropped image path
                        print(f"Object {i}: Bounding Box: ({x1}, {y1}) - ({x2}, {y2}), confidence: {conf}, class: {class_id}, Cropped Image Path: {cropped_image_path}")
        else:
            image = Image.open(path)
            results = model(image)
            filename = os.path.basename(path)
            filename_no_ext, ext = os.path.splitext(filename)
        
            for i, obj in enumerate(results.xyxy[0]):
                x1, y1, x2, y2, conf, class_id = obj.tolist()
                
                # Extract coordinates and crop image
                cropped_image = image.crop((x1, y1, x2, y2))

                # Save cropped image
                cropped_image_path = os.path.join(save_dir, f"{filename_no_ext}_cropped_{i}{ext}")
                cropped_image.save(cropped_image_path)

                # Print bounding box coordinates and cropped image path
                print(f"Object {i}: Bounding Box: ({x1}, {y1}) - ({x2}, {y2}), Cropped Image Path: {cropped_image_path}")

if __name__ == "__main__":
    input_path = Path(input("Enter the location of the image or video (0 for live view): "))

    if input_path.is_dir():
        detect_objects(path=input_path, image_dir=True)
    else:
        detect_objects(path=input_path)
