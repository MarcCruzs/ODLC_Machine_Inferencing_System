from abc import ABC, abstractmethod


class Georeferencing:
    def __init__(self):
        pass

    def calculateRealWorldLocation(self, GSDScale, Offset):
        # filler
        real_world_location = [GSDScale[i] + Offset[i] for i in range(len(GSDScale))]
        return real_world_location


# interface (i think)
class GeoreferencingGSD(ABC):
    def __init__(self, UAV_altitude, UAV_GPS):
        self.__UAV_altitude = UAV_altitude
        self.__UAV_GPS = UAV_GPS

    @abstractmethod
    def calculateLocation(self):
        pass
