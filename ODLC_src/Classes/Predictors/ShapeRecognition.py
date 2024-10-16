import subprocess
from ODLC_src.Classes.Predictors.ObjectRecognition import ObjectRecognition

class ShapeRecognition(ObjectRecognition):
    def __init__(self) -> None:
        super().__init__()

    def predict(self, image_path: str):
        # Call the parent class predict method to perform the initial object recognition
        super().predict(image_path)
        
        # Path to YOLOv5 detect.py script
        yolov5_script_path = '/path/to/yolov5/detect.py'
        
        # Construct command to run detect.py script with image_path as source
        command = ['python', yolov5_script_path, '--source', image_path]
        
        # Execute the YOLOv5 detection script
        try:
            subprocess.run(command, check=True)
            print("YOLOv5 detection completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error: YOLOv5 detection failed with error code {e.returncode}")

    def get_prediction(self):
        return super().get_prediction()
    
    def display_performance(self):
        return super().display_performance()
    
    def get_object_location(self):
        return super().get_object_location()
