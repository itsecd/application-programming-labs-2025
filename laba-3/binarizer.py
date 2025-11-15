import cv2

def binarize_image(image_path: str, threshold: int):
    """

    :param image_path: Filepath to the image to be processed.
    :param threshold: Threshold for binarization.
    :return: Binary image.
    """
    original_image = cv2.imread(image_path)
    if not original_image:
        raise FileNotFoundError(f"Error while reading file, path: {image_path}")

    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    return binary_image