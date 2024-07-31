from ODLC_src.Classes.Predictors.ObjectClassification import ObjectClassification


class ObjectRecognition(ObjectClassification):
    def __init__(self) -> None:
        super().__init__()
        self.object_location = ""

    def get_object_location(self):
        raise NotImplementedError("Subclass must implement abstract method")
