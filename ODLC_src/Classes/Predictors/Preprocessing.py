class Preprocessing():
    def __init__(self) -> None:
        pass

    def color_quantization_image(Image):
        pass


    def adjust_contrast_brightness(image_path: Image, 
                                   contrast: float = 1.0, 
                                   brightness: int = 0) -> Image:
        '''
        Adjusts contrast and brightness of a uint8 image.
        contrast: (0.0, inf) with 1.0 leaving the contrast as is
        brightness: [-255, 255] with 0 leaving the brightness as is
        '''
        brightness += int(round(255 * (1 - contrast) / 2))
        return cv2.addWeighted(image_path, contrast, image_path, 0, brightness)
    

    def kmeans_quantization(image, num_colors=5):
        pixels = image.reshape(-1, 3).astype(np.float32)

        #k equation
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 69, 1.0)
        _, labels, colors = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        colors = np.uint8(colors)
        quantized_pixels = colors[labels.flatten()]

        quantized_image = quantized_pixels.reshape(image.shape)

        return quantized_image