import logging
from ODLC_src.Classes.Predictors.ObjectClassification import ObjectClassification
from ODLC_src.Classes.Predictors.Preprocessing import adjust_contrast_brightness, kmeans_quantization
from ODLC_src.alphanumeric_classifier.text_recognition import preprocess_image

import easyocr


class AlphanumeriClassification(ObjectClassification):
    def __init__(self) -> None:
        super().__init__()

    def __preprocess_image(image_path):
        try:
            #mex josh
            testing_image = cv2.imread(image_path, 1)
            gaussian_blur =  cv2.medianBlur(testing_image, 67)
            t_image = adjust_contrast_brightness(gaussian_blur, 3, -100)

            rgb_image = cv2.cvtColor(t_image, cv2.COLOR_BGR2RGB)
            quantized_image = kmeans_quantization(rgb_image)
            quantized_image = cv2.bilateralFilter(quantized_image, 9, 75, 75)

            return quantized_image

        except Exception as e:
            logging.error(f"Error preprocessing image: {e}")
            return None
        
    def predict(self, image_path: str):
        preprocessed_image = preprocess_image(image_path)
        
        OCR_reader = ocrReader.readtext(preprocessed_image, detail=1, decoder='beamsearch')

        return super().predict(image_path)
    
    def get_prediction(self):
        return super().get_prediction()
    
    def display_performance(self):
        return super().display_performance()
    

