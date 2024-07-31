from typing import Any

from ODLC_src.Classes.Predictors.PredictorCombiner import PredictorCombiner


class CheckList:
    def __init__(self, object: PredictorCombiner) -> None:
        self.__object_list = []
        self.__object = object

    def add_object(self, object: Any):
        self.__object_list.append(object)

    def remove_object(self, object: Any):
        self.__object_list.remove(object)

    def verify_object(self, object: Any) -> bool:
        if object in self.__object_list:
            self.remove_object(object)
            return True
        else:
            return False
