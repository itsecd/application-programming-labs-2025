import cv2
import numpy as np


def binarize_image(image: np.ndarray, threshold: int):
    """
    Convert image to binary type and returns it.
    :param image: Image to be processed.
    :param threshold: Threshold for binarization.
    :return: Binary image.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

    return binary_image
