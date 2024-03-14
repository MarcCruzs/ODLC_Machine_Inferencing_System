import math

def calculate_gsd(sensor_height, focal_length, pixel_size, altitude):
    """
    Calculate Ground Sample Distance (GSD) in meters per pixel.

    Args:
    - sensor_height: Height of the sensor above ground level (in meters)
    - focal_length: Focal length of the camera lens (in millimeters)
    - pixel_size: Size of the camera sensor pixels (in micrometers)
    - altitude: Altitude of the sensor above the surface (in meters)

    Returns:
    - Ground Sample Distance (GSD) in meters per pixel
    """
    # Convert pixel size from micrometers to meters
    pixel_size_meters = pixel_size * 1e-6

    # Calculate GSD
    gsd = (sensor_height * pixel_size_meters) / (focal_length / 1000 * altitude)

    return gsd

def main():
    # Example values (replace these with actual values)
    sensor_height = 100  # meters
    focal_length = 35  # millimeters
    pixel_size = 5  # micrometers
    altitude = 500  # meters

    # Calculate GSD
    gsd = calculate_gsd(sensor_height, focal_length, pixel_size, altitude)

    print(f"Ground Sample Distance (GSD): {gsd:.4f} meters per pixel")

if __name__ == "__main__":
    main()
