import math


class GroundSampleDistance:
    def __init__(
        self,
        cameraFocalLength: float,
        cameraFocalWidth: float,
        ImageLength: float,
        ImageWidth: float,
        altitude: float,
    ):
        if not isinstance(cameraFocalLength, (float, int)):
            raise TypeError("cameraFocalLength must be a float")
        if not isinstance(cameraFocalWidth, (float, int)):
            raise TypeError("cameraFocalWidth must be a float")
        if not isinstance(ImageWidth, (float, int)):
            raise TypeError("ImageWidth must be a float")
        if not isinstance(ImageLength, (float, int)):
            raise TypeError("ImageLength must be a float")
        if not isinstance(altitude, (float, int)):
            raise TypeError("altitude must be a float")

        self.__cameraFocalLength = cameraFocalLength
        self.__cameraFocalWidth = cameraFocalWidth
        self.__ImageWidth = ImageWidth
        self.__ImageLength = ImageLength
        self.__altitude = altitude

    # Getter and Setter for cameraFocalLength
    def get_cameraFocalLength(self):
        return self.__cameraFocalLength

    def set_cameraFocalLength(self, cameraFocalLength):
        self.__cameraFocalLength = cameraFocalLength

    # Getter and Setter for cameraFocalWidth
    def get_cameraFocalWidth(self):
        return self.__cameraFocalWidth

    def set_cameraFocalWidth(self, cameraFocalWidth):
        self.__cameraFocalWidth = cameraFocalWidth

    # Getter and Setter for ImageWidth
    def get_ImageWidth(self):
        return self.__ImageWidth

    def set_ImageWidth(self, ImageWidth):
        self.__ImageWidth = ImageWidth

    # Getter and Setter for ImageLength
    def get_ImageLength(self):
        return self.__ImageLength

    def set_ImageLength(self, ImageLength):
        self.__ImageLength = ImageLength

    # Getter and Setter for altitude
    def get_altitude(self):
        return self.__altitude

    def set_altitude(self, altitude):
        self.__altitude = altitude

    def calculate_GSD(self, sensor_height: float, pixel_size: float) -> float:
        """
        Calculate the Ground Sample Distance (GSD) in meters per pixel.

        Args:
            sensor_height (float): Height of the sensor above ground level (in meters).
            focal_length (float): Focal length of the camera lens (in millimeters).
            pixel_size (float): Size of the camera sensor pixels (in micrometers).
            altitude (float): Altitude of the camera above ground level (in meters).

        Returns:
            float: The Ground Sample Distance (GSD) in meters per pixel.
        """
        # Convert pixel size from micrometers to meters
        pixel_size_meters = pixel_size * 1e-6

        # Calculate GSD
        gsd = (sensor_height * pixel_size_meters) / (
            self.__cameraFocalLength / 1000 * self.__altitude
        )

        return gsd
