from abc import ABC, abstractmethod

import Localization


class Georeferencing(Localization):
    def __init__(self) -> None:
        super().__init__()

    def calculate_location(object_location):
        pass

    def __georeference_object(GSD_scale, object_distance):
        return GSD_scale * object_distance

