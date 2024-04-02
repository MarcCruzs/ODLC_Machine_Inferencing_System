class ObjectLocation:
    def __init__(self, UAV_GPSLocation):
        if isinstance(UAV_GPSLocation, list):
            self.__UAV_GPS_ocation = UAV_GPSLocation
        else:
            raise ValueError("UAV_GPSLocation must be a list containing coordinates")

    def calculateOffset(self, ObjectPosition):
        # put filler
        offset = [a - b for a, b in zip(self.__UAV_GPSLocation, ObjectPosition)]
        print(f"Offset: {offset}")
