class ObjectClassification:
    def __init__(self) -> None:
        self.prediction = ""

    def predict(self, image_path: str):
        raise NotImplementedError("Subclass must implement abstract method")

    def get_prediction(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def display_performance(self):
        raise NotImplementedError("Subclass must implement abstract method")
