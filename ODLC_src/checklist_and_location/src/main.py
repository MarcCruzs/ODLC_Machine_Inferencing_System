from Georeferencing import GeoreferencingGSD
from ObjectLocation import ObjectLocation
from GroundSampleDistance import GroundSampleDistance
from FetchAltitude import fetch_altitude_and_gps


def main():
    # Example values (replace these with actual values)
    cameraFocalLength = 35.0  # millimeters
    cameraFocalWidth = 100.0  # millimeters
    ImageWidth = 5000  # pixels
    ImageLength = 3000  # pixels
    altitude, latitude, longitude = fetch_altitude_and_gps()

    sensor_height = 2
    pixel_size = 5

    gsd_calculator = GroundSampleDistance(
        cameraFocalLength, cameraFocalWidth, ImageWidth, ImageLength, altitude
    )

    # Calculate GSD
    gsd = gsd_calculator.calculateGSD(
        sensor_height=sensor_height, pixel_size=pixel_size
    )

    print(f"Ground Sample Distance (GSD): {gsd:.4f} meters per pixel")


if __name__ == "__main__":
    main()
